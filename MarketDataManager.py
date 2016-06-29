import string, re, urllib, sys, time

from MarketData import *
from Product import *
from OMSLogger import *

#TODO to refactor this manager so that in the future it can support different providers, for now, it's SINA
class MarketDataManager(object):
	"""
	Market Data Manager gets market data from the provider periodically
	(By design, market data manager is supposed to be running in the backend thread to get latest market data, 
		and the users can subscribe/get the market data for particular symbol/symbol list on demand
	)

	Two usage modes:
	Pre-subscription mode: Market Data Manager can push the latest data to the subscriber(this could be in a different thread)
	On-demand mode: Users get the market data for a particular symbol/symbol list on demand, it's a one-off behavior, 
					no further auto update to the users unless the symbol/symbol list is added into registered list as well
	"""
	def __init__(self, provider="SINA", interval=10):
		"""
		provider: market data provider
		interval: time interval for the manager to get latest market data from the provider periodically
		"""
		self.provider = provider
		self.interval = interval

		self.registered_symbol_list = []
		self.market_data_list = {}
	
	def __parse_market_data__(self, market_data_str):
		"""parse string format market data, accept one single line only"""
		"""return an MarketData instance if format correct, return None otherwise"""
		OMSLogger.debug("Parsing market data - {0}".format(market_data_str))
		result = re.match(".*var hq_str_(.+)=(.*)", market_data_str)
		if result is not None:			
			market_data = MarketData(result.group(1))
			value_list = string.split(result.group(2), ",")	
			market_data.name = value_list[0]
			if market_data.symbol.startswith(ProductPrefix.FUND_PREFIX):#mutual fund, get net value
				market_data.latest_net_value = float(value_list[1])
				market_data.cum_net_value = float(value_list[2])
				market_data.last_net_value = float(value_list[3])
				market_data.date, market_data.time = value_list[4:6]
			if market_data.symbol.startswith(ProductPrefix.SZ_PREFIX):#listed fund, get trade price			
				#TODO self.op, self.lcp, self.tp, self.hp, self.lp, self.bbp, self.bap, self.quantity, self.notional = value_list[0:10]
				market_data.tp = float(value_list[3])
				market_data.level2 = value_list[10:30]
				market_data.date, market_data.time = value_list[30:32]
			
			OMSLogger.debug("Successfully parsed market data!")
			return market_data
		OMSLogger.error("Passed in market data string is not well formatted")
		return None

	def __build_request__(self, symbol_list):
		if self.provider == "SINA":
			return "http://hq.sinajs.cn/list={0}".format(string.join(symbol_list, ","))

	#here we just get the raw response, and leave the response parsing later so that we don't need to block net IO
	def __request_market_data__(self, symbol_list):
		OMSLogger.debug("Sending request to get market data...")
		i = 0
		j = 50
		market_data_str_list = []
		#while j < len(symbol_list):
		feed = urllib.urlopen(self.__build_request__(symbol_list[i:j])) #TODO !!! takes aorund 2 seconds
		OMSLogger.debug(feed.geturl())
		OMSLogger.debug("Got market data response!")
		OMSLogger.debug("===>Reading each line of the response") #--->> 23 seconds to read/decode this response
		for line in feed.readlines(): #TODO !!!readlines takes around 20 seconds 
										#--> shorten the requested symbol list resolves this issue, but why?
			# OMSLogger.debug("Decoding lines ...")
			market_data = line.decode('GBK')			
			market_data_str_list.append(market_data)
		OMSLogger.debug("===>Response parsed Successfully")
		feed.close()
			# i=j
			# j+=50

		return market_data_str_list

	def __reload_market_data__(self, market_data_list, symbol_list):
		OMSLogger.debug("Reloading market data...")
		for market_data_str in self.__request_market_data__(symbol_list):
			market_data = self.__parse_market_data__(market_data_str)
			if market_data is not None:
				market_data_list[market_data.symbol] = market_data
		OMSLogger.debug("Successfully loaded/parsed new market data!")
		return True

	def start(self):
		"""start to load market data for registered products"""
		self.load_market_data = True
		while(self.load_market_data):#TODO lock
			if(len(self.registered_symbol_list) > 0):
				OMSLogger.info("Start loading market data for registered symbols...")
				self.__reload_market_data__(self.market_data_list, self.registered_symbol_list)
				OMSLogger.info("Successfully loaded market data for registered symbols!")
			time.sleep(10)			

		# print self.market_data_list
	def stop(self):
		self.load_market_data = False # TODO different thread

	def subscribe_market_data(self, symbol_list, subscriber):
		"""
		Pre-subscription Mode
		@param: subscriber is the instance of the subscriber
		@param: symbol_list is a list instance, indicating which symbols to get the market_data
		@return True if subscription correct; or False if subscription fails
		"""		
		for symbol in symbol_list:
			if symbol not in self.registered_symbol_list:
				self.registered_symbol_list.append(symbol)
		return True

	def get_market_data(self, symbol_list):
		"""
		On-demand Mode
		@param: symbol_list is a list instance, indicating which symbols to get the market_data
		@return market data dictionary, key=symbol, 
		"""		
		market_data_list = {}
		not_subscribed_symbol_list = []
		for symbol in symbol_list:
			if symbol not in self.registered_symbol_list:
				OMSLogger.debug("{0} is not registered, requesting market data once on demand!".format(symbol))
				not_subscribed_symbol_list.append(symbol)
			else:
				OMSLogger.debug("{1} is registered already, returning the latest market data from cache!".format(symbol))
				market_data_list[symbol] = self.market_data_list[symbol]

		self.__reload_market_data__(market_data_list, not_subscribed_symbol_list)
		return market_data_list