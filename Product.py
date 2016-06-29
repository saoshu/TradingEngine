from OMSLogger import *

import re

class ProductType(object):
	FUND, STRUCTURED_FUND, INDEX, STOCK = range(0, 4)

class ProductPrefix(object):
	FUND_PREFIX = "f_"
	SZ_PREFIX = "sz"
	SH_PREFIX = "sh"
	HK_PREFIX = "hk"

class Product(object):
	def __init__(self, name, symbol, product_type):
		self.name = name
		self.symbol = symbol
		self.product_type = product_type 

		#TODO differentiate SH index/SZ index/HK index
		"""
		Shanghai:
			000***	Index
			001*** 	Treasury Bond
			201***	Treasury Bond (Buy back)
			310***	Treasury Bond (Futures)
			110***	120***	Corporate Bond
			129*** 	100*** 	Convertible Bond
			500***	550***	Fund
			600***	A share STOCK			
			900***	B share STOCK
			700***	710***	701***

		Shenzhen:
			002*** 	Small and Medium-size market
			150***	160***	Fund
			300***	Growth Enterprise market
			399***	Index
		"""
		md_symbol_prefix = ""
		if re.match("[0-9]{6}", symbol):
			OMSLogger.debug("{0} is SH/SZ A share product".format(symbol))
			prefix = symbol[0:3]
			if(prefix in ("000", "600")):
				md_symbol_prefix = ProductPrefix.SH_PREFIX
			elif(prefix in ("002", "150", "160", "399")):
				md_symbol_prefix = ProductPrefix.SZ_PREFIX
		else:
			OMSLogger.debug("{0} is HK product".format(symbol))
			md_symbol_prefix = ProductPrefix.HK_PREFIX
		self.listed_md_symbol = "{0}{1}".format(md_symbol_prefix, symbol)
		
class Index(Product):
	def __init__(self, name, symbol):
		super(Index, self).__init__(name, symbol, ProductType.INDEX)

class Fund(Product):
	def __init__(self, name, symbol, underlier=None, listed=False, purchase_cost=0.0006, redeem_cost=0.0005):
		super(Fund, self).__init__(name, symbol, ProductType.FUND)
		self.purchase_cost = purchase_cost
		self.redeem_cost = redeem_cost
		#the fund is also a traditional fund who has net_value each trading day
		self.fund_md_symbol = "{0}{1}".format(ProductPrefix.FUND_PREFIX, symbol)

		self.listed = listed #True or False, some fund(ETF, StructuredFund) is also listed on the exchange
		self.underlier = underlier #product object, eg, INDEX object for an INDEX FUND

# Structured Fund, consists of three parts
# BaseFund = FundA * RatioA + FundB*RatioB
# base_tradable, by default is False cause for majority of structured fund products, base fund is non-tradable
class StructuredFund(Fund):
	def __init__(self, name, symbol, fund_a, fund_b, up_fold_px=2, underlier=None, ratio_a=1, ratio_b=1, listed=False):		
		super(StructuredFund, self).__init__(name, symbol, underlier, listed)
		self.product_type = ProductType.STRUCTURED_FUND #override product type

		self.fund_a = fund_a #product object
		self.ratio_a = ratio_a #integer
		self.fund_b = fund_b #product object
		self.ratio_b = ratio_b #integer

		self.up_fold_px = up_fold_px
		self.original_lever = (ratio_a+ratio_b)/ratio_b

		