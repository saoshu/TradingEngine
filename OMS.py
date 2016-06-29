import urllib, sys, trace, logging
from decimal import *
getcontext().prec = 3

reload(sys)
sys.setdefaultencoding("utf-8")

from MarketData import *
from MarketDataManager import *
from HistoricalMarketData import *
from Product import * 
from ProductManager import *
from Strategy import *
from OMSLogger import *

def main():
	#Initialize OMSLogger#
	# OMSLogger.init_log_system()
	OMSLogger.init_log_system(logging.DEBUG)

	#Initialize Product Manager and load all product information#
	product_mgr = ProductManager()#TODO using Singleton
	symbol_list = []
	if(product_mgr.reload_products_from_file("structured_fund_list.csv")):
		for structured_fund in product_mgr.structured_fund_list:
			symbol_list.append(structured_fund.fund_md_symbol)
			if(structured_fund.listed):#listed structured fund has trade price as well
				symbol_list.append(structured_fund.listed_md_symbol)
			symbol_list.append(structured_fund.fund_a.fund_md_symbol)
			symbol_list.append(structured_fund.fund_a.listed_md_symbol)
			symbol_list.append(structured_fund.fund_b.fund_md_symbol)
			symbol_list.append(structured_fund.fund_b.listed_md_symbol)

	# #Initialize Market Data Manager, also subscribe market data for all loaded products#
	# market_data_mgr = MarketDataManager()
	# market_data_mgr.subscribe_market_data(symbol_list, product_mgr)
	#market_data_mgr.start()
	#market_data_mgr.stop()

	#Initialize Strategy Manager, start calculating#
	# trade_strategy = StructuredFundStrategy(tf_hsi_structured)
	#trade_strategy.run()
	# gf_fund = StructuredFund("gffj", "160217", Fund("gfa", "150066"), Fund("gfb", "150067"), 1.6, Index("bond", "399481"), 7, 3)
	# StructuredFundStrategy(gf_fund).upper_fold_arbitrage(0.078, -0.01)
	for product in product_mgr.structured_fund_list:
		if product.product_type == ProductType.STRUCTURED_FUND:
			dump_fund_value_to_file(product.symbol, "20150101", "20150727")
			
	# for product in product_mgr.structured_fund_list:		
	# 	StructuredFundStrategy(product).upper_fold_arbitrage(0.056, -0.02)

if __name__ == "__main__":
	# getcontext().prec = 3
	# print getcontext()
	# print Decimal('1.06789')
	main()