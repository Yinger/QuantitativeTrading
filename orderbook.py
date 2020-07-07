import copy

class OrderBook(object) :
    # 用来存储当前时刻下的买方挂单和卖方挂单
    BIDS = 'bid' 
    ASKS = 'ask'

    def __init__(self, limit=20):
        self.limit = limit # limit，用来指示 orderbook 的 bids 和 asks 保留多少条数据

        self.bids = {}
        self.asks = {}

        self.bids_sorted = []
        self.asks_sorted = []

    # 向 orderbook 插入一条数据
    # 如果某个 price 对应的 amount 是 0，那么意味着这一条数据已经不存在了，删除即可
    def insert(self, price, amount, direction):
        if direction == self.BIDS:
            if amount == 0: 
                if price in self.bids: 
                    del self.bids[price]
            else:
                self.bids[price] = amount
        elif direction == self.ASKS:
            if amount == 0: 
                if price in self.asks: 
                    del self.asks[price]
            else:
                self.asks[price] = amount
        else: 
            print('WARNING: unknown direction {}'.format(direction))
    
    # 对 bids 和 asks 排序后截取，最后保存回 bids 和 asks
    def sort_and_truncate(self):
        # sort 
        self.bids_sorted = sorted([(price, amount) for price, amount in self.bids.items()], reverse=True) 
        self.asks_sorted = sorted([(price, amount) for price, amount in self.asks.items()])

        # truncate 
        self.bids_sorted = self.bids_sorted[:self.limit] 
        self.asks_sorted = self.asks_sorted[:self.limit]

        # copy back to bids and asks 
        self.bids = dict(self.bids_sorted) 
        self.asks = dict(self.asks_sorted)

    # 返回排过序的 bids 和 asks 数组
    def get_copy_of_bids_and_asks(self):
        return copy.deepcopy(self.bids_sorted), copy.deepcopy(self.asks_sorted)