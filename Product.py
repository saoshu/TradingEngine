
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
		
class Index(Product):
	def __init__(self, name, symbol):
		Product.__init__(name, symbol, ProductType.INDEX)

class Fund(Product):
	def __init__(self, name, symbol, listed=False, purchase_cost=0.0006, redeem_cost=0.0005):
		Product.__init__(self, name, symbol, ProductType.FUND)
		self.purchase_cost = purchase_cost
		self.redeem_cost = redeem_cost
		self.listed = listed #True or False, some fund(ETF, StructuredFund) is also listed on the exchange

# Structured Fund, consists of three parts
# BaseFund = FundA * RatioA + FundB*RatioB
# base_tradable, by default is False cause for majority of structured fund products, base fund is non-tradable
class StructuredFund(Fund):
	def __init__(self, name, symbol, fund_a, fund_b, ratio_a=1, ratio_b=1, listed=False):		
		Fund.__init__(self, name, symbol, listed)
		self.product_type = ProductType.STRUCTURED_FUND #override product type

		self.fund_a = fund_a #product object
		self.ratio_a = ratio_a #integer
		self.fund_b = fund_b #product object
		self.ratio_b = ratio_b #integer