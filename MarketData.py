
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