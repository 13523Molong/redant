
# 以下密钥信息从控制台获取
appid = "615cb71e"  # 填写控制台中获取的 APPID 信息
api_secret = "NGI2YmI0NDJmYmQyZTBjM2Q0ZDBmODBh"  # 填写控制台中获取的 APISecret 信息
api_key = "c03a937c58cb99852d48173c107a3fc2"  # 填写控制台中获取的 APIKey 信息

# 用于配置大模型版本，默认“general/generalv2”
domain = "general"  # v1.5版本
# domain = "generalv2"    # v2.0版本
# 云端环境的服务地址
Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
# Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址


text = []


# length = 0

def getText(role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text


def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text


def answer(question):
    text.clear()
    Input = question
    question = checklen(getText("user", Input))
    SparkApi.answer = ""
    # print("星火:", end="")
    SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
    getText("assistant", SparkApi.answer)
    # print(str(text))
    return text[1]['content']

#print(answer("你好"))