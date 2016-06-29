from MarketData import *
from MarketDataManager import *
from Product import *
from OMSLogger import *

from decimal import *

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


	def upper_fold_arbitrage(self, target_px_raise_ratio, target_index_raise_ratio):
		"""
		@target_px_raise_ratio:
		@target_index_raise_ratio: expected index change(in percentage) 
		"""
		if(self.product.up_fold_px == -1):
			OMSLogger.debug("up fold px for {0} is {1}, skipping calculation!".format(self.product.name, self.product.up_fold_px))
			return False

		#normally, it's only fund b can get extra profit during upper fold arbitrage
		fund = self.product.fund_b 
		symbol_list = [self.product.fund_md_symbol, fund.listed_md_symbol, fund.fund_md_symbol]
		if(fund.underlier is not None):			
			symbol_list.append(self.product.underlier.listed_md_symbol)

		market_data = MarketDataManager().get_market_data(symbol_list)
		listed_market_data = market_data[fund.listed_md_symbol] 
		fund_market_data = market_data[fund.fund_md_symbol]
		base_fund_market_data = market_data[self.product.fund_md_symbol]

		#calculate how much still required to get fold		
		net_value_increase_ratio_to_fold = self.product.up_fold_px/base_fund_market_data.latest_net_value-1
		
		if(net_value_increase_ratio_to_fold >= 0.1):
			OMSLogger.debug("net value increase ratio for {0} is {1}%, larger than 10, skipping up fold calculation".format(
				self.product.name, Decimal(net_value_increase_ratio_to_fold)*Decimal(100)))
			return False

		OMSLogger.info("net value increase ratio for {0} is {1}%, calculating up fold p&l...".format(
			self.product.name, Decimal(net_value_increase_ratio_to_fold)*Decimal(100)))
		net_value_lever = base_fund_market_data.latest_net_value*self.product.original_lever/fund_market_data.latest_net_value
		net_value_on_fold = (1+net_value_increase_ratio_to_fold*net_value_lever)*fund_market_data.latest_net_value
		# OMSLogger.debug("net_value_on_fold {0}".format(net_value_on_fold))
		#net value when it's folded 		
		fold_ratio = net_value_on_fold - 1 #normally, after upper fold, latest_net_value returns to 1
		target_return_redeem = 1*(1+target_px_raise_ratio) + fold_ratio*(1+target_index_raise_ratio) 

		# OMSLogger.debug("target_return_redeem:%s"%target_return_redeem)
		cost = listed_market_data.tp
		commission_redeem_base = 0.0006 * 2 +  0.005 * fold_ratio 
		#commission_split_base = 0.0006*2

		return_yield_redeem = Decimal(target_return_redeem/cost - 1 - commission_redeem_base) * Decimal(100)

		OMSLogger.info("return_yield for {0} up fold: {1}%".format(self.product.name, Decimal(return_yield_redeem)))
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