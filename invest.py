
import requests
import json
import base64
import hmac
import hashlib
import datetime
import time

# 使用 API 下单
# POST https://api.gemini.com/v1/order/new
def new_order():
    base_url = "https://api.sandbox.gemini.com"
    endpoint = "/v1/order/new"
    url = base_url + endpoint

    gemini_api_key = "account-QpciNCAPEKqQL6ARBr9v"
    gemini_api_secret = "28xUvgSXq4yyxSerwSVC9M6LqBM".encode()

    t = datetime.datetime.now()
    payload_nonce = str(int(time.mktime(t.timetuple())*1000))

    # 字典
    # 用来存储下单操作需要的所有的信息，也就是业务逻辑信息
    # 
    # nonce 是个单调递增的整数。
    # 当某个后来的请求的 nonce，比上一个成功收到的请求的 nouce 小或者相等的时候，Gemini 便会拒绝这次请求。
    # 这样一来，重复的包就不会被执行两次了。另一方面，这样也可以在一定程度上防止中间人攻击：
    payload = {
    "request": "/v1/order/new",
    "nonce": payload_nonce, # Gemini 交易所要求所有的通信 payload 必须带有 nonce
    "symbol": "btcusd",
    "amount": "5",
    "price": "3633.00", # limit buy，限价买单，价格为 3633 刀
    "side": "buy",
    "type": "exchange limit",
    "options": ["maker-or-cancel"]
    }

    # serialize to json formatted string
    encoded_payload = json.dumps(payload).encode()

    # 对 payload 进行 base64 和 sha384 算法非对称加密 
    # 其中 gemini_api_secret 为私钥；交易所存储着公钥，可以对发送的请求进行解密
    b64 = base64.b64encode(encoded_payload)
    signature = hmac.new(gemini_api_secret, b64, hashlib.sha384).hexdigest()

    request_headers = {
        'Content-Type': "text/plain", # Content 的类型
        'Content-Length': "0", # 长度。 Content 对应于参数 data。但是 Gemini 这里的 request 的 data 没有任何用处，因此长度为 0
        'X-GEMINI-APIKEY': gemini_api_key,
        'X-GEMINI-PAYLOAD': b64,
        'X-GEMINI-SIGNATURE': signature,
        'Cache-Control': "no-cache"
    }

    # RESTful 的 POST 请求，通过 requests.post 来实现。
    # post 接受三个参数，url、data 和 headers
    # 收到 response，订单完成
    response = requests.post(url,
                            data=None,
                            headers=request_headers)

    new_order = response.json()
    print(new_order)

if __name__ == "__main__":
	new_order()

# {'order_id': '620104488', 
#  'id': '620104488', 
#  'symbol': 'btcusd', 
#  'exchange': 'gemini', 
#  'avg_execution_price': '0.00', 
#  'side': 'buy', 
#  'type': 'exchange limit', 
#  'timestamp': '1594024609', 
#  'timestampms': 1594024609841, 
#  'is_live': True, 
#  'is_cancelled': False, 
#  'is_hidden': False, 
#  'was_forced': False, 
#  'executed_amount': '0', 
#  'options': ['maker-or-cancel'], 
#  'price': '3633.00', 
#  'original_amount': '5', 
#  'remaining_amount': '5'
# }