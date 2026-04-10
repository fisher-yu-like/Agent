# 进行API的构建：
API url= https://abcxyz.qweatherapi.com/airquality/v1/station/{LocationID}?lang=en
For me url=https://nu6apxuj6k.re.qweatherapi.com/airquality/v1/station/{LocationID}?lang=en
标头为：X-QW-Api-Key: ABCD1234EFGH
一个完整的API请求eg：curl --compressed \
-H "X-QW-Api-Key: ABCD1234EFGH" \
'https://abcxyz.qweatherapi.com/v7/weather/now?location=101010100'
那么，对于不同的需求有所改变，下面是不同task对应的API
## API
### 一、天气预警
- 请求路径：/weatheralert/v1/current/{latitude}/{longitude}
- 参数：
1. 路径参数
latitude(必选)所需位置的纬度。十进制，最多支持小数点后两位。例如 39.92
longitude(必选)所需位置的经度。十进制，最多支持小数点后两位。例如 116.41
2. 查询参数
localTime是否返回查询地点的本地时间。true 返回本地时间，false 返回UTC时间（默认）。
lang多语言设置，英文:en 中文:zh
- 请求示例:
- curl -X GET --compressed \
-H 'Authorization: Bearer your_token' \
'https://your_api_host/weatheralert/v1/current/39.90/116.40'
- {
  "metadata": {
    "tag": "ec71f87d59c5db45281fecc9f25d136f638ba414ff0a4c4e97258e6d30218aac",
    "zeroResult": false,
    "attributions": [
      "https://developer.qweather.com/attribution.html",
      "当前预警数据可能存在延迟或信息过时，以官方数据发布为准。"
    ]
  },
  "alerts": [
    {
      "id": "202510241119105837988676",
      "senderName": "临桂区气象台",
      "issuedTime": "2025-10-24T11:19+08:00",
      "messageType": {
        "code": "update",
        "supersedes": [
          "202510181140100706230391"
        ]
      },
      "eventType": {
        "name": "大风",
        "code": "1006"
      },
      "urgency": null,
      "severity": "minor",
      "certainty": null,
      "icon": "1006",
      "color": {
        "code": "blue",
        "red": 30,
        "green": 50,
        "blue": 205,
        "alpha": 1
      },
      "effectiveTime": "2025-10-24T11:19+08:00",
      "onsetTime": "2025-10-24T11:19+08:00",
      "expireTime": "2025-10-25T11:19+08:00",
      "headline": "临桂区气象台更新大风蓝色预警信号",
      "description": "临桂区气象台24日11时19分继续发布大风蓝色预警信号：预计未来24小时内临桂将出现6级（或阵风7级）以上大风，请做好防范。",
      "criteria": "24小时内可能受大风影响，平均风力可达6级以上，或者阵风7级以上；或者已经受大风影响，平均风力为6～7级，或者阵风7～8级并可能持续。",
      "responseTypes": [],
      "instruction": "1. 政府及有关部门按照职责做好防大风工作。\n2. 关好门窗，加固围板、棚架、广告牌等易被风吹动的搭建物，妥善安置易受大风影响的室外物品，遮盖建筑物资。\n3. 相关水域水上作业和过往船舶采取积极的应对措施，如回港避风或者绕道航行等。\n4. 行人注意尽量少骑自行车，刮风时不要在广告牌、临时搭建物等下面逗留。\n5. 有关部门和单位注意森林、草原等防火。"
    }
  ]
}
- metadata.tag 数据标签
metadata.zeroResult true 表示请求成功，但无数据返回，例如查询地点无预警
metadata.attributions 数据来源或声明，开发者必须将此内容与当前数据一起展示
alerts.id 本条预警信息的唯一标识
alerts.senderName 预警发布机构的名称，可能为空
alerts.issuedTime 原始预警信息生成的时间，实际发布或接收时间会略有延迟
alerts.messageType.code 预警信息性质的代码，开发者可以了解当前预警是新发布的还是对之前预警的更新。
alerts.messageType.supersedes 当前预警取代或取消后续预警ID的列表，仅在 messageType.code 为 update 或 cancel 时返回。
alerts.eventType.name 预警事件类型的名称
alerts.eventType.code 预警事件类型的代码
alerts.urgency 预警信息的紧迫程度，可能为空
alerts.severity 预警信息的严重程度
alerts.certainty 预警信息的确定性或可信度，可能为空
alerts.icon 预警对应的图标代码
alerts.color.code 预警信息的颜色代码
alerts.color.red 预警信息颜色的红色分量值（RGBA），范围 0–255
alerts.color.green 预警颜色的绿色分量值（RGBA），范围 0–255
alerts.color.blue 预警颜色的蓝色分量值（RGBA），范围 0–255
alerts.color.alpha 预警颜色的透明度分量值（RGBA），范围 0-1
alerts.effectiveTime 预警信息的生效时间，可能为空
alerts.onsetTime 预警事件预计开始的时间，可能为空
alerts.expiredTime 预警信息的失效时间
alerts.headline 预警信息的简要描述或标题
alerts.description 预警信息的详细描述
alerts.criteria 当前预警信息的触发标准或条件。仅供参考，可能滞后于官方标准。可能为空
alerts.instruction 对当前预警的防御指南或行动指导，可能为空
alerts.responseTypes 对当前预警的应对方式的类型代码，可能为空

### 二、城市搜索
- 请求路径:/geo/v2/city/lookup
- 参数:location(必选)需要查询地区的名称，支持文字、以英文逗号分隔的经度,纬度坐标（十进制，最多支持小数点后两位）、LocationID或Adcode（仅限中国城市）。例如 location=北京 或 location=116.41,39.92
- 模糊搜索，当location传递的为文字时，支持模糊搜索，即用户可以只输入城市名称一部分进行搜索，最少一个汉字或2个字符，结果将按照相关性和Rank值进行排列，便于开发或用户进行选择他们需要查看哪个城市的天气。例如location=bei，将返回与bei相关性最强的若干结果，包括黎巴嫩的贝鲁特和中国的北京市
- 重名，当location传递的为文字时，可能会出现重名的城市，例如陕西省西安市、吉林省辽源市下辖的西安区和黑龙江省牡丹江市下辖的西安区，此时会根据Rank值排序返回所有结果。在这种情况下，可以通过adm参数的方式进一步确定需要查询的城市或地区，例如location=西安&adm=黑龙江
- adm城市的上级行政区划，可设定只在某个行政区划范围内进行搜索，用于排除重名城市或对结果进行过滤。例如 adm=beijing
- 如请求参数为location=chaoyang&adm=beijing时，返回的结果只包括北京市的朝阳区，而不包括辽宁省的朝阳市

如请求参数仅为location=chaoyang时，返回的结果包括北京市的朝阳区、辽宁省的朝阳市以及长春市的朝阳区
- range搜索范围，可设定只在某个国家或地区范围内进行搜索，国家和地区名称需使用ISO 3166 所定义的国家代码。如果不设置此参数，搜索范围将在所有城市。例如 range=cn
- number返回结果的数量，取值范围1-20，默认返回10个结果。
- lang如上，以后均省略
- 请求示例:curl -X GET --compressed \
-H 'Authorization: Bearer your_token' \
'https://your_api_host/geo/v2/city/lookup?location=beij'
- {
  "code":"200",
  "location":[
    {
      "name":"北京",
      "id":"101010100",
      "lat":"39.90499",
      "lon":"116.40529",
      "adm2":"北京",
      "adm1":"北京市",
      "country":"中国",
      "tz":"Asia/Shanghai",
      "utcOffset":"+08:00",
      "isDst":"0",
      "type":"city",
      "rank":"10",
      "fxLink":"https://www.qweather.com/weather/beijing-101010100.html"
    },
    {
      "name":"海淀",
      "id":"101010200",
      "lat":"39.95607",
      "lon":"116.31032",
      "adm2":"北京",
      "adm1":"北京市",
      "country":"中国",
      "tz":"Asia/Shanghai",
      "utcOffset":"+08:00",
      "isDst":"0",
      "type":"city",
      "rank":"15",
      "fxLink":"https://www.qweather.com/weather/haidian-101010200.html"
    },
    {
      "name":"朝阳",
      "id":"101010300",
      "lat":"39.92149",
      "lon":"116.48641",
      "adm2":"北京",
      "adm1":"北京市",
      "country":"中国",
      "tz":"Asia/Shanghai",
      "utcOffset":"+08:00",
      "isDst":"0",
      "type":"city",
      "rank":"15",
      "fxLink":"https://www.qweather.com/weather/chaoyang-101010300.html"
    },
    {
      "name":"昌平",
      "id":"101010700",
      "lat":"40.21809",
      "lon":"116.23591",
      "adm2":"北京",
      "adm1":"北京市",
      "country":"中国",
      "tz":"Asia/Shanghai",
      "utcOffset":"+08:00",
      "isDst":"0",
      "type":"city",
      "rank":"23",
      "fxLink":"https://www.qweather.com/weather/changping-101010700.html"
    },
    {
      "name":"房山",
      "id":"101011200",
      "lat":"39.73554",
      "lon":"116.13916",
      "adm2":"北京",
      "adm1":"北京市",
      "country":"中国",
      "tz":"Asia/Shanghai",
      "utcOffset":"+08:00",
      "isDst":"0",
      "type":"city",
      "rank":"23",
      "fxLink":"https://www.qweather.com/weather/fangshan-101011200.html"
    },
    {
      "name":"通州",
      "id":"101010600",
      "lat":"39.90249",
      "lon":"116.65860",
      "adm2":"北京",
      "adm1":"北京市",
      "country":"中国",
      "tz":"Asia/Shanghai",
      "utcOffset":"+08:00",
      "isDst":"0",
      "type":"city",
      "rank":"23",
      "fxLink":"https://www.qweather.com/weather/tongzhou-101010600.html"
    },
    {
      "name":"丰台",
      "id":"101010900",
      "lat":"39.86364",
      "lon":"116.28696",
      "adm2":"北京",
      "adm1":"北京市",
      "country":"中国",
      "tz":"Asia/Shanghai",
      "utcOffset":"+08:00",
      "isDst":"0",
      "type":"city",
      "rank":"25",
      "fxLink":"https://www.qweather.com/weather/fengtai-101010900.html"
    },
    {
      "name":"大兴",
      "id":"101011100",
      "lat":"39.72891",
      "lon":"116.33804",
      "adm2":"北京",
      "adm1":"北京市",
      "country":"中国",
      "tz":"Asia/Shanghai",
      "utcOffset":"+08:00",
      "isDst":"0",
      "type":"city",
      "rank":"25",
      "fxLink":"https://www.qweather.com/weather/daxing-101011100.html"
    },
    {
      "name":"延庆",
      "id":"101010800",
      "lat":"40.46532",
      "lon":"115.98501",
      "adm2":"北京",
      "adm1":"北京市",
      "country":"中国",
      "tz":"Asia/Shanghai",
      "utcOffset":"+08:00",
      "isDst":"0",
      "type":"city",
      "rank":"33",
      "fxLink":"https://www.qweather.com/weather/yanqing-101010800.html"
    },
    {
      "name":"平谷",
      "id":"101011500",
      "lat":"40.14478",
      "lon":"117.11234",
      "adm2":"北京",
      "adm1":"北京市",
      "country":"中国",
      "tz":"Asia/Shanghai",
      "utcOffset":"+08:00",
      "isDst":"0",
      "type":"city",
      "rank":"33",
      "fxLink":"https://www.qweather.com/weather/pinggu-101011500.html"
    }
  ],
  "refer":{
    "sources":[
      "QWeather"
    ],
    "license":[
      "QWeather Developers License"
    ]
  }
}
- code 请参考状态码
location.name 地区/城市名称
location.id 地区/城市ID
location.lat 地区/城市纬度
location.lon 地区/城市经度
location.adm2 地区/城市的上级行政区划名称
location.adm1 地区/城市所属一级行政区域
location.country 地区/城市所属国家名称
location.tz 地区/城市所在时区
location.utcOffset 地区/城市目前与UTC时间偏移的小时数，参考详细说明
location.isDst 地区/城市是否当前处于夏令时。1 表示当前处于夏令时，0 表示当前不是夏令时。
location.type 地区/城市的属性
location.rank 地区评分
location.fxLink 该地区的天气预报网页链接，便于嵌入你的网站或应用
refer.sources 原始数据来源，或数据源说明，可能为空
refer.license 数据许可或版权声明，可能为空

### 三、天气指数
- 请求路径：/v7/indices/{days}t
- 参数：路径参数
days(必选)预报天数，支持最多3天预报，可选值：
1d 1天预报。
3d 3天预报。
查询参数
location(必选)需要查询地区的LocationID或以英文逗号分隔的经度,纬度坐标（十进制，最多支持小数点后两位），LocationID可通过GeoAPI获取。例如 location=101010100 或 location=116.41,39.92
type(必选)生活指数的类型ID，包括洗车指数、穿衣指数、钓鱼指数等。可以一次性获取多个类型的生活指数，多个类型用英文,分割。例如type=3,5。具体生活指数的ID和等级参考天气指数信息。各项生活指数并非适用于所有城市。
- curl -X GET --compressed \
-H 'Authorization: Bearer your_token' \
'https://your_api_host/v7/indices/1d?type=1,2&location=101010100'
- {
  "code": "200",
  "updateTime": "2021-12-16T18:35+08:00",
  "fxLink": "http://hfx.link/2ax2",
  "daily": [
    {
      "date": "2021-12-16",
      "type": "1",
      "name": "运动指数",
      "level": "3",
      "category": "较不宜",
      "text": "天气较好，但考虑天气寒冷，风力较强，推荐您进行室内运动，若户外运动请注意保暖并做好准备活动。"
    },
    {
      "date": "2021-12-16",
      "type": "2",
      "name": "洗车指数",
      "level": "3",
      "category": "较不宜",
      "text": "较不宜洗车，未来一天无雨，风力较大，如果执意擦洗汽车，要做好蒙上污垢的心理准备。"
    }
  ],
  "refer": {
    "sources": [
      "QWeather"
    ],
    "license": [
      "QWeather Developers License"
    ]
  }
}
- code 请参考状态码
updateTime 当前API的最近更新时间
fxLink 当前数据的响应式页面，便于嵌入网站或应用
daily.date 预报日期
daily.type 生活指数类型ID
daily.name 生活指数类型的名称
daily.level 生活指数预报等级
daily.category 生活指数预报级别名称
daily.text 生活指数预报的详细描述，可能为空
refer.sources 原始数据来源，或数据源说明，可能为空
refer.license 数据许可或版权声明，可能为空
- 等级和类型：
- 天气指数类型	API类型值	iOS Indices	Android Indices
全部天气指数	0	ALL	ALL
运动指数	1	SPT	SPT
洗车指数	2	CW	CW
穿衣指数	3	DRSG	DRSG
钓鱼指数	4	FIS	FIS
紫外线指数	5	UV	UV
旅游指数	6	TRA	TRA
花粉过敏指数	7	AG	AG
舒适度指数	8	COMF	COMF
感冒指数	9	FLU	FLU
空气污染扩散条件指数	10	AP	AP
空调开启指数	11	AC	AC
太阳镜指数	12	GL	GL
化妆指数	13	MU	MU
晾晒指数	14	DC	DC
交通指数	15	PTFC	PTFC
防晒指数	16	SPI	SPI
- 天气指数类型	级别名称(对应等级数值)
运动指数	适宜(1)、较适宜(2)、较不宜(3)
洗车指数	适宜(1)、较适宜(2)、较不宜(3)、不宜(4)
穿衣指数	寒冷(1)、冷(2)、较冷(3)、较舒适(4)、舒适(5)、热(6)、炎热(7)
钓鱼指数	适宜(1)、较适宜(2)、不宜(3)
紫外线指数	最弱(1)、弱(2)、中等(3)、强(4)、很强(5)
旅游指数	适宜(1)、较适宜(2)、一般(3)、较不宜(4)、不适宜(5)
花粉过敏指数	极不易发(1)、不易发(2)、较易发(3)、易发(4)、极易发(5)
舒适度指数	舒适(1)、较舒适(2)、较不舒适(3)、很不舒适(4)、极不舒适(5)、不舒适(6)、非常不舒适(7)
感冒指数	少发(1)、较易发(2)、易发(3)、极易发(4)
空气污染扩散条件指数	优(1)、良(2)、中(3)、较差(4)、很差(5)
空调开启指数	长时间开启(1)、部分时间开启(2)、较少开启(3)、开启制暖空调(4)
太阳镜指数	不需要(1)、需要(2)、必要(3)、很必要(4)、非常必要(5)
化妆指数	保湿(1)、保湿防晒(2)、去油防晒(3)、防脱水防晒(4)、去油(5)、防脱水(6)、防晒(7)、滋润保湿(8)
晾晒指数	极适宜(1)、适宜(2)、基本适宜(3)、不太适宜(4)、不宜(5)、不适宜(6)
交通指数	良好(1)、较好(2)、一般(3)、较差(4)、很差(5)
防晒指数	弱(1)、较弱(2)、中等(3)、强(4)、极强(5)

### 四、分钟级降水
- /v7/minutely/5m
- 查询参数
location(必选)需要查询地区的以英文逗号分隔的经度,纬度坐标（十进制，最多支持小数点后两位）。例如 location=116.41,39.92
- curl -X GET --compressed \
-H 'Authorization: Bearer your_token' \
'https://your_api_host/v7/minutely/5m?location=116.38,39.91'
- {
  "code": "200",
  "updateTime": "2021-12-16T18:55+08:00",
  "fxLink": "https://www.qweather.com",
  "summary": "95分钟后雨就停了",
  "minutely": [
    {
      "fxTime": "2021-12-16T18:55+08:00",
      "precip": "0.15",
      "type": "rain"
    },
    {
      "fxTime": "2021-12-16T19:00+08:00",
      "precip": "0.23",
      "type": "rain"
    },
    {
      "fxTime": "2021-12-16T19:05+08:00",
      "precip": "0.21",
      "type": "rain"
    },
    {
      "fxTime": "2021-12-16T19:10+08:00",
      "precip": "0.17",
      "type": "rain"
    },
    {
      "fxTime": "2021-12-16T19:15+08:00",
      "precip": "0.18",
      "type": "rain"
    },
    {
      "fxTime": "2021-12-16T19:20+08:00",
      "precip": "0.24",
      "type": "rain"
    },
    {
      "fxTime": "2021-12-16T19:25+08:00",
      "precip": "0.31",
      "type": "rain"
    },
    {
      "fxTime": "2021-12-16T19:30+08:00",
      "precip": "0.37",
      "type": "rain"
    },
    {
      "fxTime": "2021-12-16T19:35+08:00",
      "precip": "0.41",
      "type": "rain"
    },
    {
      "fxTime": "2021-12-16T19:40+08:00",
      "precip": "0.43",
      "type": "rain"
    },
    {
      "fxTime": "2021-12-16T19:45+08:00",
      "precip": "0.41",
      "type": "rain"
    },
    {
      "fxTime": "2021-12-16T19:50+08:00",
      "precip": "0.36",
      "type": "rain"
    },
    {
      "fxTime": "2021-12-16T19:55+08:00",
      "precip": "0.32",
      "type": "rain"
    },
    {
      "fxTime": "2021-12-16T20:00+08:00",
      "precip": "0.27",
      "type": "rain"
    },
    {
      "fxTime": "2021-12-16T20:05+08:00",
      "precip": "0.22",
      "type": "rain"
    },
    {
      "fxTime": "2021-12-16T20:10+08:00",
      "precip": "0.17",
      "type": "rain"
    },
    {
      "fxTime": "2021-12-16T20:15+08:00",
      "precip": "0.11",
      "type": "rain"
    },
    {
      "fxTime": "2021-12-16T20:20+08:00",
      "precip": "0.06",
      "type": "rain"
    },
    {
      "fxTime": "2021-12-16T20:25+08:00",
      "precip": "0.0",
      "type": "rain"
    },
    {
      "fxTime": "2021-12-16T20:30+08:00",
      "precip": "0.0",
      "type": "rain"
    },
    {
      "fxTime": "2021-12-16T20:35+08:00",
      "precip": "0.0",
      "type": "rain"
    },
    {
      "fxTime": "2021-12-16T20:40+08:00",
      "precip": "0.0",
      "type": "rain"
    },
    {
      "fxTime": "2021-12-16T20:45+08:00",
      "precip": "0.0",
      "type": "rain"
    },
    {
      "fxTime": "2021-12-16T20:50+08:00",
      "precip": "0.0",
      "type": "rain"
    }
  ],
  "refer": {
    "sources": [
      "QWeather"
    ],
    "license": [
      "QWeather Developers License"
    ]
  }
}
- code 请参考状态码
updateTime 当前API的最近更新时间
fxLink 当前数据的响应式页面，便于嵌入网站或应用
summary 分钟降水描述
minutely.fxTime 预报时间
minutely.precip 5分钟累计降水量，单位毫米
minutely.type 降水类型：rain = 雨，snow = 雪
refer.sources 原始数据来源，或数据源说明，可能为空
refer.license 数据许可或版权声明，可能为空

### 五、实时天气
- /v7/weather/now
- 查询参数
location(必选)需要查询地区的LocationID或以英文逗号分隔的经度,纬度坐标（十进制，最多支持小数点后两位），LocationID可通过GeoAPI获取。例如 location=101010100 或 location=116.41,39.92
lang多语言设置，请阅读多语言文档，了解我们的多语言是如何工作、如何设置以及数据是否支持多语言。
unit数据单位设置，可选值包括unit=m（公制单位，默认）和unit=i（英制单位）。更多选项和说明参考度量衡单位。
- curl -X GET --compressed \
-H 'Authorization: Bearer your_token' \
'https://your_api_host/v7/weather/now?location=101010100'
- {
  "code": "200",
  "updateTime": "2020-06-30T22:00+08:00",
  "fxLink": "http://hfx.link/2ax1",
  "now": {
    "obsTime": "2020-06-30T21:40+08:00",
    "temp": "24",
    "feelsLike": "26",
    "icon": "101",
    "text": "多云",
    "wind360": "123",
    "windDir": "东南风",
    "windScale": "1",
    "windSpeed": "3",
    "humidity": "72",
    "precip": "0.0",
    "pressure": "1003",
    "vis": "16",
    "cloud": "10",
    "dew": "21"
  },
  "refer": {
    "sources": [
      "QWeather",
      "NMC",
      "ECMWF"
    ],
    "license": [
      "QWeather Developers License"
    ]
  }
}
- code 请参考状态码
updateTime 当前API的最近更新时间
fxLink 当前数据的响应式页面，便于嵌入网站或应用
now.obsTime 数据观测时间
now.temp 温度，默认单位：摄氏度
now.feelsLike 体感温度，默认单位：摄氏度
now.icon 天气状况的图标代码，另请参考天气图标项目
now.text 天气状况的文字描述，包括阴晴雨雪等天气状态的描述
now.wind360 风向360角度
now.windDir 风向
now.windScale 风力等级
now.windSpeed 风速，公里/小时
now.humidity 相对湿度，百分比数值
now.precip 过去1小时降水量，默认单位：毫米
now.pressure 大气压强，默认单位：百帕
now.vis 能见度，默认单位：公里
now.cloud 云量，百分比数值。可能为空
now.dew 露点温度。可能为空
refer.sources 原始数据来源，或数据源说明，可能为空
refer.license 数据许可或版权声明，可能为空

### 六、实施空气质量
- /airquality/v1/current/{latitude}/{longitude}
-  路径参数
latitude(必选)所需位置的纬度。十进制，最多支持小数点后两位。例如 39.92
longitude(必选)所需位置的经度。十进制，最多支持小数点后两位。例如 116.41
- curl -X GET --compressed \
-H 'Authorization: Bearer your_token' \
'https://your_api_host/airquality/v1/current/39.90/116.40'
- {
  "metadata": {
    "tag": "d75a323239766b831889e8020cba5aca9b90fca5080a1175c3487fd8acb06e84"
  },
  "indexes": [
    {
      "code": "us-epa",
      "name": "AQI (US)",
      "aqi": 46,
      "aqiDisplay": "46",
      "level": "1",
      "category": "Good",
      "color": {
        "red": 0,
        "green": 228,
        "blue": 0,
        "alpha": 1
      },
      "primaryPollutant": {
        "code": "pm2p5",
        "name": "PM 2.5",
        "fullName": "Fine particulate matter (<2.5µm)"
      },
      "health": {
        "effect": "No health effects.",
        "advice": {
          "generalPopulation": "Everyone can continue their outdoor activities normally.",
          "sensitivePopulation": "Everyone can continue their outdoor activities normally."
        }
      }
    },
    {
      "code": "qaqi",
      "name": "QAQI",
      "aqi": 0.9,
      "aqiDisplay": "0.9",
      "level": "1",
      "category": "Excellent",
      "color": {
        "red": 80,
        "green": 240,
        "blue": 230,
        "alpha": 1
      },
      "primaryPollutant": {
        "code": "pm2p5",
        "name": "PM 2.5",
        "fullName": "Fine particulate matter (<2.5µm)"
      },
      "health": {
        "effect": "No health implications.",
        "advice": {
          "generalPopulation": "Enjoy your outdoor activities.",
          "sensitivePopulation": "Enjoy your outdoor activities."
        }
      }
    }
  ],
  "pollutants": [
    {
      "code": "pm2p5",
      "name": "PM 2.5",
      "fullName": "Fine particulate matter (<2.5µm)",
      "concentration": {
        "value": 11.0,
        "unit": "μg/m3"
      },
      "subIndexes": [
        {
          "code": "us-epa",
          "aqi": 46,
          "aqiDisplay": "46"
        },
        {
          "code": "qaqi",
          "aqi": 0.9,
          "aqiDisplay": "0.9"
        }
      ]
    },
    {
      "code": "pm10",
      "name": "PM 10",
      "fullName": "Inhalable particulate matter (<10µm)",
      "concentration": {
        "value": 12.0,
        "unit": "μg/m3"
      },
      "subIndexes": [
        {
          "code": "us-epa",
          "aqi": 12,
          "aqiDisplay": "12"
        },
        {
          "code": "qaqi",
          "aqi": 0.5,
          "aqiDisplay": "0.5"
        }
      ]
    },
    {
      "code": "no2",
      "name": "NO2",
      "fullName": "Nitrogen dioxide",
      "concentration": {
        "value": 6.77,
        "unit": "ppb"
      },
      "subIndexes": [
        {
          "code": "us-epa",
          "aqi": 7,
          "aqiDisplay": "7"
        },
        {
          "code": "qaqi",
          "aqi": 0.1,
          "aqiDisplay": "0.1"
        }
      ]
    },
    {
      "code": "o3",
      "name": "O3",
      "fullName": "Ozone",
      "concentration": {
        "value": 0.02,
        "unit": "ppb"
      },
      "subIndexes": [
        {
          "code": "us-epa",
          "aqi": 21,
          "aqiDisplay": "21"
        },
        {
          "code": "qaqi",
          "aqi": 0.2,
          "aqiDisplay": "0.2"
        }
      ]
    },
    {
      "code": "co",
      "name": "CO",
      "fullName": "Carbon monoxide",
      "concentration": {
        "value": 0.25,
        "unit": "ppm"
      },
      "subIndexes": [
        {
          "code": "us-epa",
          "aqi": 3,
          "aqiDisplay": "3"
        },
        {
          "code": "qaqi",
          "aqi": 0.1,
          "aqiDisplay": "0.1"
        }
      ]
    }
  ],
  "stations": [
    {
      "id": "P51762",
      "name": "North Holywood"
    },
    {
      "id": "P58056",
      "name": "Pasadena"
    },
    {
      "id": "P57327",
      "name": "Los Angeles - N. Main Street"
    }
  ]
}
- metadata.tag 数据标签
indexes.code 空气质量指数Code
indexes.name 空气质量指数的名字
indexes.aqi 空气质量指数的值
indexes.aqiDisplay 空气质量指数的值的文本显示
indexes.level 空气质量指数等级，可能为空
indexes.category 空气质量指数类别，可能为空
indexes.color.red 空气质量指数的颜色，RGBA中的red
indexes.color.green 空气质量指数的颜色，RGBA中的green
indexes.color.blue 空气质量指数的颜色，RGBA中的blue
indexes.color.alpha 空气质量指数的颜色，RGBA中的alpah
indexes.primaryPollutant.code 首要污染物的Code，可能为空
indexes.primaryPollutant.name 首要污染物的名字，可能为空
indexes.primaryPollutant.fullName 首要污染物的全称，可能为空
indexes.health.effect 空气质量对健康的影响，可能为空
indexes.health.advice.generalPopulation 对一般人群的健康指导意见，可能为空
indexes.health.advice.sensitivePopulation 对敏感人群的健康指导意见，可能为空
pollutants.code 污染物的Code
pollutants.name 污染物的名字
pollutants.fullName 污染物的全称
pollutants.concentration.value 污染物的浓度值
pollutants.concentration.unit 污染物的浓度值的单位
pollutants.subIndexes.code 污染物的分指数的Code，可能为空
pollutants.subIndexes.aqi 污染物的分指数的数值，可能为空
pollutants.subIndexes.aqiDisplay 污染物的分指数数值的显示名称
stations.id AQI相关联的监测站Location ID，可能为空
stations.name AQI相关联的监测站名称
- 支持的国家或地区 
空气质量v1及未来版本支持中国、美国、亚洲和欧洲大部分国家，并将逐步拓展新的国家和地区。

ISO 3166-1	国家或地区	支持的AQIs
ad	安道尔	eu-eea
be	比利时	eu-eea
bg	保加利亚	eu-eea
ca	加拿大	ca-eccc
cn	中国	cn-mee cn-mee-1h
hr	克罗地亚	eu-eea
cz	捷克	eu-eea
dk	丹麦	eu-eea
fi	芬兰	eu-eea
fr	法国	fr-atmo eu-eea
de	德国	eu-eea
gi	直布罗陀	eu-eea
gr	希腊	eu-eea
hk	中国香港	hk-epd
hu	匈牙利	eu-eea
ie	爱尔兰	eu-eea
jp	日本	jp-moe
kr	韩国	kr-moe
lv	拉脱维亚	eu-eea
lt	立陶宛	eu-eea
mo	中国澳门	mo-smg
mt	马耳他	eu-eea
nl	荷兰	eu-eea
mk	北马其顿	eu-eea
no	挪威	eu-eea
pl	波兰	eu-eea
pt	葡萄牙	eu-eea
ro	罗马尼亚	eu-eea
rs	塞尔维亚	eu-eea
sg	新加坡	sg-nea sg-nea-pm1h
sk	斯洛伐克	eu-eea
si	斯洛文尼亚	eu-eea
es	西班牙	eu-eea
se	瑞典	eu-eea
ch	瑞士	eu-eea
tw	中国台湾省	tw-me tw-me-1h
th	泰国	th-pcd
gb	英国	gb-defra eu-eea
us	美国	us-epa us-epa-nc
支持的空气质量指数 
和风天气支持两种AQI类型，并在API中返回最多两个AQI数据：通用AQI与本地AQI。
- 本地AQI 
本地空气质量一般由各国或地区环境部门进行监控和管理，并且根据当地的实际情况制定空气质量指数的标准，这些指数具有不同的标准和计算方法，并且有可能会发布多个标准的空气质量指数。

AQI列表 
以下是我们支持的空气质量指数以及它们对应的取值范围、类别等：

AQI	取值范围	(级别) 类别	颜色
AQHI (CA)
ca-eccc
污染物: o3, no2, pm2p5
1	(1) 低风险	(0,204,255)
2	(1) 低风险	(0,153,204)
3	(1) 低风险	(0,102,153)
4	(2) 中风险	(255,255,0)
5	(2) 中风险	(255,204,0)
6	(2) 中风险	(255,153,51)
7	(3) 高风险	(255,102,102)
8	(3) 高风险	(255,0,0)
9	(3) 高风险	(204,0,0)
10	(3) 高风险	(153,0,0)
10+	(4) 极高风险	(102,0,0)
AQI (CN)
cn-mee
污染物: o3, co, so2, no2, pm10, pm2p5
0 ~ 50	(1) 优	(0,228,0)
51 ~ 100	(2) 良	(255,255,0)
101 ~ 150	(3) 轻度污染	(255,126,0)
151 ~ 200	(4) 中度污染	(255,0,0)
201 ~ 300	(5) 重度污染	(153,0,76)
301 ~ 500	(6) 严重污染	(126,0,35)
AQI-1H (CN)
cn-mee-1h
污染物: o3, co, so2, no2, pm10, pm2p5
0 ~ 50	(1) 优	(0,228,0)
51 ~ 100	(2) 良	(255,255,0)
101 ~ 150	(3) 轻度污染	(255,126,0)
151 ~ 200	(4) 中度污染	(255,0,0)
201 ~ 300	(5) 重度污染	(153,0,76)
301 ~ 500	(6) 严重污染	(126,0,35)
EAQI (EU)
eu-eea
污染物: o3, so2, no2, pm10, pm2p5
1	(1) 优	(80,240,230)
2	(2) 良	(80,204,170)
3	(3) 中	(240,230,65)
4	(4) 差	(255,80,80)
5	(5) 很差	(150,0,50)
6	(6) 极差	(135,33,129)
Indice ATMO (FR)
fr-atmo
污染物: o3, so2, no2, pm10, pm2p5
1	(1) 好	(80,240,230)
2	(2) 一般	(80,204,170)
3	(3) 不好	(240,230,65)
4	(4) 差	(255,80,80)
5	(5) 很差	(150,0,50)
6	(6) 极差	(135,33,129)
DAQI (GB)
gb-defra
污染物: o3, so2, no2, pm10, pm2p5
1	(1) 低	(156,255,156)
2	(1) 低	(49,255,0)
3	(1) 低	(49,207,0)
4	(2) 中	(255,255,0)
5	(2) 中	(255,207,0)
6	(2) 中	(255,154,0)
7	(3) 高	(255,100,100)
8	(3) 高	(255,0,0)
9	(3) 高	(153,0,0)
10	(4) 严重	(206,48,255)
AQHI (HK)
hk-epd
污染物: o3, co, so2, no2, pm10, pm2p5
1 ~ 3	(1) 低	(77,183,72)
4 ~ 6	(2) 中	(249,166,26)
7	(3) 高	(237,27,36)
8 ~ 10	(4) 甚高	(159,71,33)
10+	(5) 严重	(0,0,0)
AQI (JP)
jp-moe
污染物: o3, so2, no, no2, nmhc, pm10, pm2p5
1	(1) 蓝色	(0,51,255)
2	(2) 青色	(0,255,255)
3	(3) 绿色	(51,255,0)
4	(4) 黄色/注意	(255,255,0)
5	(5) 橙色/警报	(255,102,0)
6	(6) 红色/严重警报	(255,0,0)
CAI (KR)
kr-moe
污染物: o3, co, so2, no2, pm10, pm2p5
0 ~ 50	(1) 好	(0,0,255)
51 ~ 100	(2) 中等	(0,255,0)
101 ~ 250	(3) 不健康	(255,255,0)
251 ~ 500	(4) 非常不健康	(255,0,0)
AQI (MO)
mo-smg
污染物: o3, co, so2, no2, pm10, pm2p5
0 ~ 50	(1) 良好	(38,255,48)
51 ~ 100	(2) 普通	(255,255,55)
101 ~ 200	(3) 不良	(252,121,34)
201 ~ 300	(4) 非常不良	(255,1,0)
301 ~ 400	(5) 严重	(227,0,152)
401 ~ 500	(6) 有害	(124,0,6)
QAQI
qaqi
污染物: o3, co, so2, no2, pm10, pm2p5
0 ~ 2.0	(1) 优	(32,130,80)
2.1 ~ 4.0	(2) 良	(0,91,156)
4.1 ~ 5.0	(3) 中等	(242,169,0)
5.1 ~ 7.0	(4) 差	(234,107,33)
7.1 ~ 9.0	(5) 很差	(202,40,36)
9.1 ~ 10	(6) 极差	(128,71,130)
PSI 24H (SG)
sg-nea
污染物: o3, co, so2, no2, pm10, pm2p5
0 ~ 50	(1) 良好水平	(123,196,102)
51 ~ 100	(2) 适中水平	(102,186,232)
101 ~ 200	(3) 不健康水平	(254,214,49)
201 ~ 300	(4) 非常不健康水平	(250,166,53)
301 ~ 500	(5) 危险水平	(237,29,47)
1-Hour PM2.5 (SG)
sg-nea-pm1h
污染物: pm2p5
0 ~ 55	(1) 等级 1 (正常)	(213,238,252)
56 ~ 150	(2) 等级2 (偏高)	(188,209,238)
151 ~ 250	(3) 等级3 (高)	(212,209,233)
251+	(4) 等级4 (非常高)	(176,172,213)
AQI (TH)
th-pcd
污染物: o3, co, so2, no2, pm10, pm2p5
0 ~ 25	(1) 优秀	(59,204,255)
25 ~ 50	(2) 良好	(146,208,80)
51 ~ 100	(3) 中等	(255,255,0)
101 ~ 200	(4) 不健康	(255,162,0)
201+	(5) 非常不健康	(240,70,70)
Daily AQI (TW)
tw-me
污染物: o3, co, so2, no2, pm10, pm2p5
0 ~ 50	(1) 良好	(0,255,0)
51 ~ 100	(2) 普通	(255,255,0)
101 ~ 150	(3) 对敏感人群不健康	(255,126,0)
151 ~ 200	(4) 对所有人群不健康	(255,0,0)
201 ~ 300	(5) 非常不健康	(128,0,128)
301 ~ 500	(6) 危害	(126,0,35)
Real-time AQI (TW)
tw-me-1h
污染物: o3, co, so2, no2, pm10, pm2p5
0 ~ 50	(1) 良好	(0,255,0)
51 ~ 100	(2) 普通	(255,255,0)
101 ~ 150	(3) 对敏感人群不健康	(255,126,0)
151 ~ 200	(4) 对所有人群不健康	(255,0,0)
201 ~ 300	(5) 非常不健康	(128,0,128)
301 ~ 500	(6) 危害	(126,0,35)
AQI (US)
us-epa
污染物: o3, co, so2, no2, pm10, pm2p5
0 ~ 50	(1) 好	(0,228,0)
51 ~ 100	(2) 中等	(255,255,0)
101 ~ 150	(3) 不适于敏感人群	(255,126,0)
151 ~ 200	(4) 不健康	(255,0,0)
201 ~ 300	(5) 非常不健康	(153,0,76)
301 ~ 500	(6) 危险	(126,0,35)
AQI NowCast (US)
us-epa-nc
污染物: o3, co, so2, no2, pm10, pm2p5
0 ~ 50	(1) 好	(0,228,0)
51 ~ 100	(2) 中等	(255,255,0)
101 ~ 150	(3) 不适于敏感人群	(255,126,0)
151 ~ 200	(4) 不健康	(255,0,0)
201 ~ 300	(5) 非常不健康	(153,0,76)
301 ~ 500	(6) 危险	(126,0,35)
下载完整表格：aqis.csv

AQI的值 
空气质量指数并非一定是数字，一些国家的标准或在某些等级时，AQI使用文字进行描述。例如加拿大AQHI的取值范围是1-10+，显然“10+”是一个文本。为了便于计算和符合规范的显示，我们为AQI的值提供了两种表达方式：

aqi 数字类型的值，这包括了本身是数字表达的AQI，也包括用文字表达的AQI，我们将其转化为数字，以便于开发者进行计算。
aqiDisplay 字符串类型的值，用于直接显示。这也是当地AQI的标准格式，因此在向你的用户展示时，建议使用这个字段。
在加拿大的例子中，如果当前空气质量的类别是“极高风险”：

{
  "indexes": [
    {
      "aqi": 11,
      "aqiDisplay": "10+"
    }
  ]
}
-  污染物 
空气质量由空气污染物确定，污染物浓度越高，对人体的危害越大。污染物包括固体颗粒、滴液和气体的混合物，它们有多种来源，例如家庭燃料燃烧、工业生产、交通废气、发电、露天焚烧、沙尘等。《世卫组织全球空气质量指南》提到的污染物有PM2.5、PM10、O3、NO2、SO2和CO，然而各国和地区的环境部门对于污染物有不同的定义，例如中国空气质量要求计算6种污染物，欧盟则要求计算5种污染物。

注意：在实践中，AQI中的污染物并不一致，在一些地区也可能无法提供污染物的详细数据，这是因为：

当地规范对污染物的标准不同
监测站故障或被关闭
监测站不支持某些污染物的监控
法律法规的要求
另一方面，污染物浓度的单位也不尽相同，请参考下表了解污染物的名称和它们可用的单位。

code	名称	全称	单位(新版)	单位(旧版)
pm10	PM 10	颗粒物（粒径小于等于10µm）	
μg/m³
μg/m³
pm2p5	PM 2.5	颗粒物（粒径小于等于2.5µm）	
μg/m³
μg/m³
co	CO	一氧化碳	
mg/m³
μg/m³
ppm
μg/m³
no	NO	一氧化氮	
ppm
-
no2	NO2	二氧化氮	
μg/m³
ppb
ppm
μg/m³
so2	SO2	二氧化硫	
μg/m³
ppb
ppm
μg/m³
o3	O3	臭氧	
μg/m³
ppb
ppm
μg/m³
nmhc	NMHC	非甲烷总烃	
ppmC
-
污染物分指数 
污染物分指数是各项污染物的空气质量指数。通常，我们需要先计算分指数，然后最差的分指数代表即为当前的AQI数值，例如：

AQI = max {SUB-INDEX1,SUB-INDEX2,SUB-INDEX3,...SUB-INDEXn}
通过污染物分指数，我们可以了解当前空气质量各项污染物的水平，也用于挑选出当前空气质量的罪魁祸首-首要污染物。

首要污染物 
浓度值最高或污染物分指数最差的污染物是首要污染物，代表导致当前空气污染的主要成分。

提示：根据各国或地区的标准，首要污染物可能无法被计算，此时首要污染物为空。

空气质量监测站 
在大多数地点，我们会参考附近空气质量监测站的数据进行AQI的计算，此时API中将返回这些参考的监测站ID和名字。

你可以使用监测站数据API获取具体监测站所测量的污染物浓度值。

注意：监测站可能由于各种原因无法提供数据，例如故障、维护等，且无法预知何时恢复或是否能恢复。因此请不要完全依赖监测站数据，或将监测站作为枚举值，或作为固定展示。

中国空气质量指数说明 
在中国地区的空气质量数据，请参考下列说明：

空气质量指数的计算按照《环境空气质量指数（AQI）技术规定（试行）（HJ 633—2012）》为准。
不支持QAQI
空气质量预报中，不支持污染物的详细数据。
当污染物分指数<50时，AQI (CN) 的首要污染物均为空。
所提供的空气质量数据仅为参考值，未经过完整的审核程序进行修订和确认，不适用评价达标状况或任何正式评估。请以中国环境监测总站发布的空气质量数据为准。