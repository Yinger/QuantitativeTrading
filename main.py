# from crawler import Crawler
from utils import read_file
from backtest import Backtest
from exchangeAPI import ExchangeAPI
from smacross import SmaCross

if __name__ == "__main__":
    # crawler = Crawler(symbol='BTCUSD', output_file='BTCUSD.txt')
    BTCUSD = read_file('BTCUSD_GEMINI.csv')
    ret = Backtest(BTCUSD, SmaCross, ExchangeAPI, 110000.0, 0.003).run()
    print(ret)