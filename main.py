import os
from ollama import chat
from ollama import ChatResponse
'''
#食用方法1
content=input("输入问题：")
response:ChatResponse=chat(model='qwen2.5:7b',messages=[
    {
        'role':'user',
        'content':content
    },
])
#print(response['message']['content'])
print(response.message.content)
'''

#食用方法2：流式响应
'''
stream=chat(
    model='qwen2.5:7b',
    messages=[{'role':'user','content':'为什么天空是蓝色的'}],
    stream=True,
)
for chunk in stream:
    print(chunk.message.content, end='', flush=True)'''

#接下来进行天气agent的构建，采用的api基础是和风天气url=https://dev.qweather.com/
#进行单次尝试
'''
import requests
def get_weather(location):
    proxies = {
        "http": "http://127.0.0.1:9674",
        "https": "http://127.0.0.1:9674",
    }
    url="https://nu6apxuj6k.re.qweatherapi.com/geo/v2/city/lookup"
    headers={
        "X-QW-Api-Key": "1bfe188918d2433785cd5b4833aeec8a",
        "Accept-Encoding": "gzip"
    }
    params={
        "location":location,
        "lang":"zh"
    }
    try:
        respose= requests.get(url,headers=headers,params=params,proxies=proxies,timeout=5)
        respose.raise_for_status()

        data=respose.json()
        return data
    except requests.exceptions.RequestException as e:
        return f"请求发生错误: {e}"

result = get_weather("北京")
print(result)
'''
#单次成功，接下来考虑进行整体研究
import  requests

class QWeather:
    host = "nu6apxuj6k.re.qweatherapi.com"
    def __init__(self):
        #self.key=key
        self.geo_host="nu6apxuj6k.re.qweatherapi.com"
        self.called_endpoints=set()

    def _request(self,url,params):
        endpoint=url.split('/')[-1]
        if endpoint in self.called_endpoints:
            return f"状态：接口 {endpoint} 此前请求失败，已拦截重复请求。"
        headers={
            "X-QW-Api-Key": "1bfe188918d2433785cd5b4833aeec8a",
            "Accept-Encoding": "gzip"
        }
        try:
            proxies = {
                "http": "http://127.0.0.1:9674",
                "https": "http://127.0.0.1:9674",
             }
            response=requests.get(url, params, headers=headers, proxies=proxies,timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.called_endpoints.add(endpoint)  # 记录失败
            return f"错误：{endpoint} 请求失败，原因：{str(e)}"
Weather=QWeather()
from  langchain.tools import  tool
import  re
from pydantic.v1 import BaseModel, Field
@tool(description="通过城市名称查询该城市的地理信息。这是执行任何天气查询的第一步")
def search_city(location:str):
    """通过城市名称查询该城市的地理信息。
    这是执行任何天气查询的第一步。
    返回信息包含：Location ID (用于查天气)、经度(longitude)与纬度(latitude)。
    输入参数：城市中文名（例如：北京)。"""
    data=Weather._request(f"https://{Weather.host}/geo/v2/city/lookup",{"location": location})
    if isinstance(data,dict) and data.get("code")=="200":
        city=data["location"][0]
        return f"城市：{city['name']}, 该城市的编号是{city['id']}, 纬度数值为{city['lat']}, 经度数值为{city['lon']}, 地区：{city['adm1']}"
    return "找不到该城市，请检查输入。"

@tool(description="获取指定城市的实时天气数据")
def get_weather_now(location_id:str):
    """获取指定城市的实时天气数据（如天气现象、温度、感官温度）。
    输入参数：必须是 search_city 返回的 Location ID中内容，参数 location_id 必须是纯数字字符串（如 101010100）"""
    clean_id = "".join(re.findall(r'\d+', str(location_id)))#这条我不会 正则表达式？
    data=Weather._request(f"https://{Weather.host}/v7/weather/now",{"location": clean_id})
    if isinstance(data,dict) and data.get("code")=="200":
        n=data["now"]
        return  f"实时：{n['text']}, 温度：{n['temp']}℃, 体感：{n['feelsLike']}℃。"
    return str(data)

@tool(description="查询实时的空气质量指数 (AQI) 及主要污染物")
def get_air_quality(coordinates: str):
    """根据坐标查询空气质量。
    参数 coordinates 必须传入格式为 "经度,纬度" 的字符串，而不是json文件,不要出现"coordinates"。
    例如："116.41,39.92"""

    clean_input = coordinates.replace('"', '').replace("'", "").replace(" ", "")
    if ":" in clean_input:
        clean_input = clean_input.split(":")[-1]
    if "=" in clean_input:
        clean_input = clean_input.split("=")[-1]

    latitude,  longitude = clean_input.split(",")
    latitude=round(float(latitude),2)
    longitude=round(float(longitude),2)
    data=Weather._request(f"https://{Weather.host}/airquality/v1/current/{latitude}/{longitude}",{})
    if isinstance(data, dict) and data.get("code") == "200":
        a = data["indexes"]
        return f"AQI：{a[0]['aqi']}, 级别：{a[0]['category']}, 主要污染物：{a['primaryPollutant']['code']}。"
    else:
        return str(data)

@tool(description="查询未来两小时的分钟级降水预报")
def get_precip_minutely(coordinates: str):

    """根据经纬度查询未来两小时的分钟级降水预报，判断是否会下雨。
    参数 coordinates 必须传入格式为 "经度,纬度" 的字符串，而不是json文件,不要出现"coordinates"。
    例如："116.41,39.92"""

    clean_input = coordinates.replace('"', '').replace("'", "").replace(" ", "")
    if ":" in clean_input:
        clean_input = clean_input.split(":")[-1]
    if "=" in clean_input:
        clean_input = clean_input.split("=")[-1]

    latitude,  longitude = clean_input.split(",")
    latitude=round(float(latitude),2)
    longitude=round(float(longitude),2)
    location_param = f"{longitude},{latitude}"
    data=Weather._request(f"https://{Weather.host}/v7/minutely/5m",{"location": location_param})
    if isinstance(data, dict) and data.get("code") == "200":
        return f"降水预报：{data['summary']}"
    return str(data)

@tool(description="查询当前生效的天气灾害预警")
def get_weather_warning(coordinates: str):
    """根据经纬度查询当前生效的天气灾害预警（如暴雨、高温、大风预警）。
    参数 coordinates 必须传入格式为 "经度,纬度" 的字符串，而不是json文件,不要出现"coordinates"。
    例如："116.41,39.92"""
    clean_input = coordinates.replace('"', '').replace("'", "").replace(" ", "")
    if ":" in clean_input:
        clean_input = clean_input.split(":")[-1]
    if "=" in clean_input:
        clean_input = clean_input.split("=")[-1]

    latitude, longitude = clean_input.split(",")
    latitude = round(float(latitude), 2)
    longitude = round(float(longitude), 2)
    data = Weather._request(f"https://{Weather.host}/weatheralert/v1/current/{latitude}/{longitude}",{})
    if isinstance(data, dict) and data.get("code") == "200":
        warnings = data.get("alerts", [])
        if not warnings: return "目前无天气预警。"
        return f"预警：{warnings[0]['description']}"
    else:
        return str(data)

@tool(description="查询生活指数")
def get_weather_indices(location_id: str):
    """查询生活指数，包含穿衣、防晒、紫外线等建议。
        输入参数：必须是 search_city 返回的 Location ID
        参数 location_id 必须是纯数字字符串（如 101010100）"""
    days="1d"
    clean_id = "".join(re.findall(r'\d+', str(location_id)))
    data = Weather._request(f"https://{Weather.host}/v7/indices/{days}", {"type": "0","location": clean_id})
    if isinstance(data, dict) and data.get("code") == "200":
        indices = [f"{i['name']}: {i['text']}" for i in data["daily"]]
        return " | ".join(indices)
    return str(data)
tools = [search_city, get_weather_now, get_air_quality, get_precip_minutely, get_weather_warning, get_weather_indices]

from langchain_ollama import ChatOllama
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents import create_react_agent
from langchain_core.prompts import PromptTemplate
llm=ChatOllama(
    model="qwen2.5:7b",
    temperature=0,
    num_ctx=4096,
    base_url="http://localhost:11434",
    #stop=["Observation:", "Observation：", "Final Answer:"]
)


# 直接把 ReAct 的思考逻辑写在本地，不依赖任何外部 hub 包
template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,      # 开启后你可以看到 Qwen 思考的过程
    handle_parsing_errors=True,
    max_iterations=10   # 允许它最多进行 10 步推理
)

# 5. 执行查询
query = "帮我查查合肥的天气、空气质量，未来两小时有雨吗？有没有预警和穿衣建议？"
agent_executor.invoke({"input": query})
