"""
Historical market data for structured Fund
"""
class StructuredFundHisotricalMarketData(object):
	def __init__(self, date, netvalue_a, px_a, premium_a, netvalue_b, px_b, premium_b, netvalue_base, premium_base):
		self.date = date
		self.netvalue_a = netvalue_a
		self.price_a = px_a
		self.premium_a = premium_a
		self.netvalue_b = netvalue_b
		self.px_b = px_b
		self.premium_b = premium_b
		self.netvalue_base = netvalue_base
		self.premium_base = premium_base

"""
Real time market data for general equity product
"""
class MarketData(object):
	def __init__(self, symbol):
		self.symbol = symbol
		#Market Data name/value pairs
		self.name = None #product name/description
		self.op = None #today open price
		self.lcp = None #last close price
		self.tp = None #current trading price
		self.hp = None #highest price so far
		self.lp = None #lowest price so far
		self.bbp = None #current best bid(buy) price
		self.bap = None #current best ask(sell) price
		self.quantity = None #traded quantity so far, in shares, not in lot
		self.notional = None #traded notional value so far
		self.level2 = None #List, level 2 market data
		self.date = None 
		self.time = None	

		#market data for Mutual Fund
		self.latest_net_value = None #net value on last trade day
		self.cum_net_value =  None #cumulate net value as of now
		self.last_net_value = None #estimated_net_value for the day before last trade day