'''本代码参考url=https://github.com/Hoper-J/AI-Guide-and-Demos-zh_CN/blob/master/PaperNotes/Demos/%E5%8A%A8%E6%89%8B%E5%AE%9E%E7%8E%B0%20Transformer.ipynb
《动手实现Transformer》完成，并加以自己的理解，参数调整尝试以及可视化处理，
并在此基础上实现手撕self-attention'''

#Let's go!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
import torch
import torch.nn as nn
import  torch.nn.functional as F
import  math
import  matplotlib.pyplot as plt

#缩放点积注意力机制 Scaled Dot-Product Attention
def scaled_dot_product_attention(Q,K,V,mask=None):
    """
        缩放点积注意力计算。

        参数:
            Q: 查询矩阵 (batch_size, seq_len_q, embed_size)
            K: 键矩阵 (batch_size, seq_len_k, embed_size)
            V: 值矩阵 (batch_size, seq_len_v, embed_size)
            mask: 掩码矩阵，用于屏蔽不应该关注的位置 (可选)

        返回:
            output: 注意力加权后的输出矩阵
            attention_weights: 注意力权重矩阵

        PS:batch_size就是有多少句话分别进行计算
        当batch=1，q就是一个seq*embed的二维矩阵但是其中都要进行embedding操作
        """
    embed_size=Q.size(-1) #embed_size 由于Q有三维，embed_size为最后一维，对应的-1

    scores= torch.matmul(Q,K.transpose(-2,-1))/math.sqrt(embed_size)

    #掩码矩阵
    if mask is not None:
        scores=scores.masked_fill(mask==0,float('-inf'))
    attention_weights =F.softmax(scores,dim=-1)#每个行对应一个token 然后分别归一化打分
    output=torch.matmul(attention_weights,V)

    return output,attention_weights

#多头注意力机制 Multi-Head Attention
class MultiHeadAttention(nn.Module):
    def __init__(self,d_model,h):
        """
                多头注意力机制：每个头单独定义线性层。

                参数:
                    d_model: 输入序列的嵌入维度。
                    h: 注意力头的数量。
                """
        super(MultiHeadAttention,self).__init__()
        assert d_model %h == 0 ,   "d_model 必须能被 h 整除。"

        self.d_model=d_model
        self.h=h

        # “共享”的 Q, K, V 线性层
        self.w_q = nn.Linear(d_model, d_model)
        self.w_k = nn.Linear(d_model, d_model)
        self.w_v = nn.Linear(d_model, d_model)

        # 输出线性层，将多头拼接后的输出映射回 d_model
        self.fc_out = nn.Linear(d_model, d_model)
    def forward(self,q,k,v,mask=None):
        """
               前向传播函数。

               参数:
                   q: 查询矩阵 (batch_size, seq_len_q, d_model)
                   k: 键矩阵 (batch_size, seq_len_k, d_model)
                   v: 值矩阵 (batch_size, seq_len_v, d_model)
                   mask: 掩码矩阵 (batch_size, 1, seq_len_q, seq_len_k)

               返回:
                   out: 注意力加权后的输出
                   attention_weights: 注意力权重矩阵
               """
        batch_size=q.size(0)

        seq_len_q=q.size(1)
        seq_len_k=k.size(1)

        Q=self.w_q(q).view(batch_size,seq_len_q,self.h,-1).transpose(1,2)
        K=self.w_k(k).view(batch_size,seq_len_k,self.h,-1).transpose(1,2)
        V=self.w_v(v).view(batch_size,seq_len_k,self.h,-1).transpose(1,2)

        scaled_attention,_=scaled_dot_product_attention(Q,K,V,mask)

        concat_out=scaled_attention.transpose(1,2).contiguous().view(batch_size,-1,self.d_model)

        out=self.fc_out(concat_out)

        return out

#FFN  Position-wise Feed-Forward Networks 前馈神经网络

class PositionwiseFeedForward(nn.Module):
    def __init__(self,d_model,d_ff,dropout=0.1):
        """
                位置前馈网络。

                参数:
                    d_model: 输入和输出向量的维度
                    d_ff: FFN 隐藏层的维度，或者说中间层
                    dropout: 随机失活率（Dropout），即随机屏蔽部分神经元的输出，用于防止过拟合

                （实际上论文并没有确切地提到在这个模块使用 dropout，所以注释）
                """
        super(PositionwiseFeedForward,self).__init__()
        self.w_1=nn.Linear(d_model,d_ff)
        self.w_2=nn.Linear(d_ff,d_model)
        #self.dropout =nn.Dropout(dropout)

    def forward(self,x):
        # 先经过第一个线性层和 ReLU，然后经过第二个线性层
        return self.w_2(self.w_1(x).relu())

#残差连接和层归一化 Add&Norm

class ResidualConnection(nn.Module):
    def __init__(self,dropout=0.1):
        """
                残差连接，用于在每个子层后添加残差连接和 Dropout。

                参数:
                    dropout: Dropout 概率，用于在残差连接前应用于子层输出，防止过拟合。
                """
        super(ResidualConnection,self).__init__()
        self.dropout=nn.Dropout(p=dropout)
    def forward(self,x,sublayer):
        """
               前向传播函数。

               参数:
                   x: 残差连接的输入张量，形状为 (batch_size, seq_len, d_model)。
                   sublayer: 子层模块的函数，多头注意力或前馈网络。

               返回:
                   经过残差连接和 Dropout 处理后的张量，形状为 (batch_size, seq_len, d_model)。
               """
        return x+self.dropout(sublayer(x))

class LayerNorm(nn.Module):
    def __init__(self,feature_size,epsilon=1e-9):
        """
                层归一化，用于对最后一个维度进行归一化。

                参数:
                    feature_size: 输入特征的维度大小，即归一化的特征维度。
                    epsilon: 防止除零的小常数。
                """
        super(LayerNorm,self).__init__()
        self.gamma=nn.Parameter(torch.ones(feature_size))#只有注册为Parameter的张量才会被更新
        self.beta=nn.Parameter(torch.zeros(feature_size))
        self.epsilon=epsilon

    def forward(self,x ):
        mean=x.mean(dim=-1,keepdim=True)
        std=x.std(dim=-1,keepdims=True)
        return self.gamma*(x-mean)/(std+self.epsilon)+self.beta#这里归一化没有加平方？
#注意这里没有采用nn.Linear因为*和矩阵乘法是不同的

class SublayerConnection(nn.Module):
    def __init__(self,feature_size,dropout=0.1,epsilon=1e-9):
        super(SublayerConnection,self).__init__()
        self.residual=ResidualConnection(dropout)
        self.norm=LayerNorm(feature_size,epsilon)

    def forward(self,x,sublayer):
        return self.norm(self.residual(x,sublayer))

#嵌入 Embeddings

class Embeddings(nn.Module):
    def __init__(self,vocab_size,d_model):
        super(Embeddings,self).__init__()
        self.embed=nn.Embedding(vocab_size,d_model)
        self.scale_factor=math.sqrt(d_model)
    def forward(self,x):
        return self.embed(x)*self.scale_factor


#位置编码，由于模型需要分辨出“你爱我和我爱你”
class PositionalEncoding(nn.Module):
    def __init__(self,d_model,dropout=0.1,max_len=5000):
        """
           位置编码，为输入序列中的每个位置添加唯一的位置表示，以引入位置信息。

           参数:
               d_model: 嵌入维度，即每个位置的编码向量的维度。
               dropout: 位置编码后应用的 Dropout 概率。
               max_len: 位置编码的最大长度，适应不同长度的输入序列。
           """
        super(PositionalEncoding,self).__init__()
        self.dropout=nn.Dropout(p=dropout) # 正如论文 5.4 节所提到的，需要将 Dropout 应用在 embedding 和 positional encoding 相加的时候

        pe=torch.zeros(max_len,d_model)
        position=torch.arange(0,max_len).unsqueeze(1)

        # 计算每个维度对应的频率
        div_term = torch.exp(
            torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model)
        )

        # 将位置和频率结合，计算 sin 和 cos
        pe[:, 0::2] = torch.sin(position * div_term)  # 偶数维度
        pe[:, 1::2] = torch.cos(position * div_term)  # 奇数维度

        # 增加一个维度，方便后续与输入相加，形状变为 (1, max_len, d_model)
        pe = pe.unsqueeze(0)

        # 将位置编码注册为模型的缓冲区，不作为参数更新
        self.register_buffer('pe', pe)

    def forward(self,x):
        x=x+self.pe[:, :x.size(1), :]

        return self.dropout(x)

#编码器输入处理

class SourceEmbedding(nn.Module):
    def __init__(self,src_vocab_size,d_model,dropout=0.1):
        """
                源序列嵌入，将输入的 token 序列转换为嵌入向量并添加位置编码。

                参数:
                    src_vocab_size: 源语言词汇表的大小
                    d_model: 嵌入向量的维度
                    dropout: 在位置编码后应用的 Dropout 概率
                """
        super(SourceEmbedding,self).__init__()
        self.embed=Embeddings(src_vocab_size,d_model)
        self.positional_encoding=PositionalEncoding(d_model,dropout)

    def forward(self,x):
        x=self.embed(x)
        return self.positional_encoding(x)

class TargetEmbedding(nn.Module):
    def __init__(self,tgt_vocab_size,d_model,dropout=0.1):
        """
               目标序列嵌入，将目标序列的 token ID 转换为嵌入向量并添加位置编码。

               参数:
                   tgt_vocab_size: 目标语言词汇表的大小
                   d_model: 嵌入向量的维度
                   dropout: 在位置编码后应用的 Dropout 概率
               """
        super(TargetEmbedding, self).__init__()
        self.embed = Embeddings(tgt_vocab_size, d_model)  # 词嵌入层
        self.positional_encoding = PositionalEncoding(d_model, dropout)  # 位置编码层

    def forward(self, x):
        """
        前向传播函数。

        参数:
            x: 目标序列的输入张量，形状为 (batch_size, seq_len_tgt)，其中每个元素是 token ID。

        返回:
            添加位置编码后的嵌入向量，形状为 (batch_size, seq_len_tgt, d_model)。
        """
        x = self.embed(x)  # 生成词嵌入 (batch_size, seq_len_tgt, d_model)
        return self.positional_encoding(x)  # 加入位置编码
#掩码
def create_padding_mask(seq,pad_token=0):
    mask=(seq!=pad_token).unsqueeze(1).unsqueeze(2)
    return mask

#未来信息掩码
def create_look_ahead_mask(size):
    mask=torch.tril(torch.ones(size,size)).type(torch.bool)
    return mask

#组合掩码
def create_decoder_mask(tgt_seq,pad_token=0):
    padding_mask=create_padding_mask(tgt_seq,pad_token)
    look_ahead_mask=create_look_ahead_mask(tgt_seq.size(1)).to(tgt_seq.device)
    combined_mask=look_ahead_mask.unsqueeze(0)& padding_mask
    return combined_mask

#开始搭框架

class EncodeLayer(nn.Module):
    """
           编码器层。

           参数:
               d_model: 嵌入维度
               h: 多头注意力的头数
               d_ff: 前馈神经网络的隐藏层维度
               dropout: Dropout 概率
           """
    def __init__(self,d_model,h,d_ff,dropout):
        super(EncodeLayer,self).__init__()
        self.self_attn=MultiHeadAttention(d_model,h)
        self.feed_forward=PositionwiseFeedForward(d_model, d_ff, dropout)

        # 定义两个子层连接，分别用于多头自注意力和前馈神经网络（对应模型架构图中的两个残差连接）
        self.sublayers=nn.ModuleList([SublayerConnection(d_model,dropout)for _ in range(2)])
        self.d_model=d_model

    def forward(self,x,src_mask):
        x=self.sublayers[0](x,lambda x:self.self_attn(x,x,x,src_mask))
        x=self.sublayers[1](x,self.feed_forward)
        return x

class DecodeLayer(nn.Module):
    def __init__(self,d_model,h,d_ff,dropout):
        super(DecodeLayer,self).__init__()
        self.self_attn=MultiHeadAttention(d_model,h)
        self.cross_attn=MultiHeadAttention(d_model, h)
        self.feed_forward=PositionwiseFeedForward(d_model,d_ff,dropout)

        self.sublayers=nn.ModuleList([SublayerConnection(d_model,dropout)for _ in range(3)])
        self.d_model=d_model
    def forward(self,x,memory,src_mask,tgt_mask):
        """
                前向传播函数。
                参数:
                    x: 解码器输入 (batch_size, seq_len_tgt, d_model)
                    memory: 编码器输出 (batch_size, seq_len_src, d_model)
                    src_mask: 源序列掩码，用于交叉注意力
                    tgt_mask: 目标序列掩码，用于自注意力
                返回:
                    x: 解码器层的输出
                """
        # 第一个子层：掩码多头自注意力（Masked Multi-Head Self-Attention）
        x = self.sublayers[0](x, lambda x: self.self_attn(x, x, x, tgt_mask))

        # 第二个子层：交叉多头注意力（Multi-Head Cross-Attention），使用编码器的输出 memory
        x = self.sublayers[1](x, lambda x: self.cross_attn(x, memory, memory, src_mask))

        # 第三个子层：前馈神经网络
        x = self.sublayers[2](x, self.feed_forward)

        return x

#编码器 Encoder
class Encoder(nn.Module):
    def __init__(self,d_model,N,h,d_ff,dropout=0.1):
        """
                编码器，由 N 个 EncoderLayer 堆叠而成。

                参数:
                    d_model: 嵌入维度
                    N: 编码器层的数量
                    h: 多头注意力的头数
                    d_ff: 前馈神经网络的隐藏层维度
                    dropout: Dropout 概率
                """
        super(Encoder,self).__init__()
        self.layers=nn.ModuleList([
            EncodeLayer(d_model,h, d_ff, dropout) for _ in range(N)
        ])
        self.norm=LayerNorm(d_model)

    def forward(self,x,mask):
        for layer in self.layers:
            x=layer(x,mask)
        return self.norm(x)

class Decoder(nn.Module):
    def __init__(self,d_model,N,h,d_ff,dropout=0.1):
        super(Decoder,self).__init__()
        self.layers=nn.ModuleList([DecodeLayer(d_model, h, d_ff, dropout)for _ in range(N)])
        self.norm=LayerNorm(d_model)
    def forward(self,x,memory,src_mask,tgt_mask):
        for layer in self.layers:
            x=layer(x,memory,src_mask,tgt_mask)
        return self.norm(x)

class Transformer(nn.Module):
    def __init__(self,src_vocab_size,tgt_vocab_size,d_model,N,h,d_ff,dropout=0.1):
        super(Transformer,self).__init__()

        self.src_embedding=SourceEmbedding(src_vocab_size, d_model, dropout)
        self.tgt_embedding = TargetEmbedding(tgt_vocab_size, d_model, dropout)

        self.encoder = Encoder(d_model, N, h, d_ff, dropout)
        self.decoder = Decoder(d_model, N, h, d_ff, dropout)

        self.fc_out = nn.Linear(d_model, tgt_vocab_size)

    def forward(self,src,tgt):
        src_mask=create_padding_mask(src)
        tgt_mask=create_decoder_mask(tgt)

        enc_output=self.encoder(self.src_embedding(src), src_mask)
        dec_output = self.decoder(self.tgt_embedding(tgt), enc_output, src_mask, tgt_mask)
        output = self.fc_out(dec_output)

        return output






