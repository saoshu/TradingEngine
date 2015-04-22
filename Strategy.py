from MarketData import *
from Product import *
from OMSLogger import *

import time

class Strategy(object):

	def __init__(self):
		pass

	#cost is the cost ratio, not the notional value
	def calc_pnl(self, buy_price, sell_price, cost):
		if buy_price==0:
			return 0
		return sell_price/buy_price - 1 - cost

	def run(self):
		pass

class StructuredFundStrategy(Strategy):
	def __init__(self, product):
		self.product = product #Structured Product object
	
	def merge_arbitrage(self):
		OMSLogger.debug("trying merge arbitrage")
		merge_price = self.market_data_a.tp * self.product.ratio_a + self.market_data_b.tp * self.product.ratio_b
		OMSLogger.debug("price a = {0} ; price b = {1}; merge_price = {2}".format(self.market_data_a.tp, self.market_data_b.tp, merge_price))
		base_price = self.market_data_base.tp * (self.product.ratio_a + self.product.ratio_b)
		OMSLogger.debug("base_price = {0}".format(base_price))
		cost = 0.005 + 0.0012
		return_yield = self.calc_pnl(merge_price, base_price, cost)
		OMSLogger.debug("return yield is {0}".format(return_yield))
		if (return_yield > 0):
			OMSLogger.info("suggest doing merge arbitrage")
			return True
		return False

	def split_arbitrage(self):
		OMSLogger.debug("trying split arbitrage")
		split_price = self.market_data_a.tp * self.product.ratio_a + self.market_data_b.tp * self.product.ratio_b
		base_price = self.market_data_base.tp * (self.product.ratio_a + self.product.ratio_b)
		cost = 0.012 + 0.0012
		return_yield = self.calc_pnl(base_price, split_price, cost)
		OMSLogger.debug("return yield is {0}".format(return_yield))
		if (return_yield > 0):
			OMSLogger.info("suggest doing split arbitrage")
			return True
		return False

	def lower_fold_arbitrage(self):
		return False

	def upper_fold_arbitrage(self):
		fund_b = self.product.fund_b
		return False
	
	def run(self):
		self.market_data_base = MarketData(self.product.symbol_base)
		self.market_data_a = MarketData(self.product.fund_a.symbol)
		self.market_data_b = MarketData(self.product.fund_b.symbol)
		while(True):
			if(self.market_data_base.get() and self.market_data_a.get() and self.market_data_b.get()):
				self.merge_arbitrage()
				self.split_arbitrage()
			time.sleep(10) #market date update interval, 1 s