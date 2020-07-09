import websocket # pip install websocket_client
import ssl
import json
import time

from orderbook import OrderBook

class Crawler:
    def __init__(self, symbol, output_file):
        self.orderbook = OrderBook(limit=10)
        self.output_file = output_file

        self.ws = websocket.WebSocketApp('wss://api.gemini.com/v1/marketdata/{}'.format(symbol), on_message = lambda ws, message: self.on_message(message))
        self.ws.run_forever(sslopt={'cert_reqs': ssl.CERT_NONE})
    
    def on_message(self, message):
        # 对收到的信息进行处理，然后送给 orderbook
        data = json.loads(message)
        for event in data['events']:
            price, amount, direction = float(event['price']), float(event['remaining']), event['side']
            self.orderbook.insert(price, amount, direction)
        
        # 整理 orderbook，排序，只选取我们需要的前几个
        self.orderbook.sort_and_truncate()

        # 输出到文件
        with open(self.output_file, 'a+') as f:
            bids, asks = self.orderbook.get_copy_of_bids_and_asks()
            output = { 
                'bids': bids, 
                'asks': asks, 
                'ts': int(time.time() * 1000)
                 }
            f.write(json.dumps(output) + '\n')