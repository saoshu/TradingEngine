import urllib, sys, trace

reload(sys)
sys.setdefaultencoding("utf-8")

from MarketData import *
from MarketDataManager import *
from Product import * 
from ProductManager import *
from Strategy import *
from OMSLogger import *

def main():
	#Initialize OMSLogger#
	OMSLogger.init_log_system()

	#Initialize Product Manager and load all product information#
	product_mgr = ProductManager()#TODO using Singleton
	symbol_list = []
	if(product_mgr.reload_products_from_file("structured_fund_list.csv")):
		for structured_fund in product_mgr.structured_fund_list:
			symbol_list.append("{0}{1}".format(ProductPrefix.FUND_PREFIX, structured_fund.symbol))
			if(structured_fund.listed):#listed structured fund has trade price as well
				symbol_list.append("{0}{1}".format(ProductPrefix.SZ_PREFIX, structured_fund.symbol))
			symbol_list.append("{0}{1}".format(ProductPrefix.FUND_PREFIX, structured_fund.fund_a.symbol))
			symbol_list.append("{0}{1}".format(ProductPrefix.SZ_PREFIX, structured_fund.fund_a.symbol))
			symbol_list.append("{0}{1}".format(ProductPrefix.FUND_PREFIX, structured_fund.fund_b.symbol))
			symbol_list.append("{0}{1}".format(ProductPrefix.SZ_PREFIX, structured_fund.fund_b.symbol))

	#Initialize Market Data Manager, also subscribe market data for all loaded products#
	market_data_mgr = MarketDataManager()
	market_data_mgr.subscribe_market_data(symbol_list, product_mgr)
	market_data_mgr.start()
	market_data_mgr.stop()

	#Initialize Strategy Manager, start calculating#
	# trade_strategy = StructuredFundStrategy(tf_hsi_structured)
	#trade_strategy.run()

if __name__ == "__main__":
	main()