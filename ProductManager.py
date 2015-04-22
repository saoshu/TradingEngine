import string, trace, urllib, httplib

from Product import *
from OMSLogger import *

class ProductManager(object):
	def __init__(self):
		self.structured_fund_list = None

	def reload_products_from_file(self, file_name):
		"""Load all products from a formatted file"""
		OMSLogger.info("Loadding products from file %s ..." % file_name)
		with open(file_name) as structured_fund_list_file:
			fund_list = structured_fund_list_file.readlines()			
			self.structured_fund_list = []
			for fund_str in fund_list[1:]:#first line is title, so we get fund from the second line, index=1
				fund = string.strip(fund_str.decode("GBK"))
				symbol_base, name_base, underlier_name, underlier, up_fold_px, down_fold_px, expiration_date,\
				symbol_a, name_a, current_rate, next_rate, rate_formula, \
				symbol_b, name_b, ratio, \
				purchase_cost, redeem_cost, listed \
				= string.split(fund, ",") 

				fund_a = Fund(name_a, symbol_a)
				fund_b = Fund(name_b, symbol_b)
				ratio_a_str, ratio_b_str = string.split(ratio, ":")
				self.structured_fund_list.append(StructuredFund(name_base, symbol_base, fund_a, fund_b, int(ratio_a_str), int(ratio_b_str), listed=="Y"))
		OMSLogger.info("{0} products successfully loaded!".format(len(self.structured_fund_list)))
		# fundinfo = urllib.urlopen("http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=8&CATALOGID=1105&tab1PAGENUM=1&ENCODE=1&TABKEY=tab1")
		# print fundinfo.info()
		
		# ....
		# params = urllib.urlencode({'ACTIONID': '8', 'CATALOGID': '1105', 'tab1PAGENUM': '1', 'ENCODE': '1', 'TABKEY': 'tab1'})
		# url = "/szseWeb/FrontController.szse?%s" % params
		# headers = {"Accept": "application/vnd.ms-excel"}
		# conn = httplib.HTTPConnection("www.szse.cn")
		# conn.request("GET", url, None, headers)
		# response = conn.getresponse()
		# print response.read().decode('GBK')
		# conn.close()

		if self.structured_fund_list is not None:
			return True
			print self.structured_fund_list
		else:
			return False
