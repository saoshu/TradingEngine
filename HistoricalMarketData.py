import urllib, urllib2, sys, re

from OMSLogger import *
from MarketData import StructuredFundHisotricalMarketData

reload(sys)
sys.setdefaultencoding("utf-8")

def load_abcfund_response(request_url):
	# print request_url
	response = urllib2.urlopen(request_url)
	matcher = re.match(".*charset=(.*)", response.headers['Content-type'])
	charset = 'GBK' # default charset
	if matcher is not None:
		charset = matcher.group(1)

	result = []
	for line in response.readlines():
		result.append(line.decode(charset))

	return result


"""
get historical market data for a given fund during a given period

return a list of data, in which each row is the data for an individual trading day
"""
def load_data_from_abcfund(fund_symbol, from_date, to_date):
	req_url = "http://www.abcfund.cn/data/historicalpremium.php?fundcode=%s&d1=%s&d2=%s" % (fund_symbol, from_date, to_date)
	response = load_abcfund_response(req_url)
	values = []
	for line in response:
		matcher = re.match(".*tbody><tr>(.*)</tr>.*", line)
		if matcher is not None:
			value = matcher.group(1) 
			for row in value.split("</tr><tr>"):
				formated_row = row.replace("</td><td>", ",").replace("<td>", "").replace("</td>", "")\
							 .replace("<font color=green>", "").replace("<font color=red>", "").replace("</font>","")
				values.append(formated_row)
	return values

def dump_fund_value_to_file(fund_symbol, from_date, to_date):
	OMSLogger.debug("dumping value for %s to file" % fund_symbol)
	file_name = fund_symbol + ".csv"
	title = u"date,netvalue(A),price(A),overload(A)(%),netvalue(B),price(B),overload(B)(%),basevalue,overload(overall)(%)"
	value = load_data_from_abcfund(fund_symbol, from_date, to_date)
	with open(file_name, 'wb') as feed:
		feed.write(title)
		feed.write("\n")
		for line in value:
			feed.write(line)
			feed.write("\n")

#dump value to memory for calculation
def dump_fund_value(fund_symbol, from_date, to_date):
	OMSLogger.debug("dumping value for %s" % fund_symbol)
	for line in load_data_from_abcfund(fund_symbol, from_date, to_date):
		pass #TODO do nothing for now

"""
TODO: this should ideally be put into a seperate class/file

It calculates, for a given structured fund, in a trading period(from_date, to_date), the distribution of premium value of A
"""
def calc_premium_ratio(fund_symbol, from_date, to_date):
	value = load_data_from_abcfund(fund_symbol, from_date, to_date)
	premium_value_map = {}
	count = 0
	for line in value:
		count += 1
		columns = line.split(",")
		premium_a = int(float(columns[3]) * -1000)/100
		if premium_a not in premium_value_map.keys():
			premium_value_map[premium_a] = 1
		else:
			premium_value_map[premium_a] += 1

	return (value[-1].split(',')[3], premium_value_map)


def save_ratio_into_file(fund_symbol, from_date, to_date):
	file_name = fund_symbol+"_cal.csv"
	premium_value_map = calc_premium_ratio(fund_symbol, from_date, to_date)[1]
	with open(file_name, 'wb') as feed:
		for premium in premium_value_map.keys():
			feed.write("%s, %s" % (premium, premium_value_map[premium]))
			feed.write("\n")

if __name__ == '__main__':	

	fund_list = (("161024", 157), ("163115", 156), ("160630", 167), ("161026", 156), ("165522", 152))
	from datetime import *
	date_format = "%Y%m%d"
	to_date = date.today().strftime(date_format)
	date_one_month_back = date.today()-timedelta(days=30)
	date_three_month_back = date.today()-timedelta(days=30*3)
	date_six_month_back = date.today()-timedelta(days=30*6)
	date_one_year_back = date.today()-timedelta(days=30*12)
	from_date_list = (("Recent Month", date_one_month_back.strftime(date_format)),\
		("Recent 3 Month", date_three_month_back.strftime(date_format)), \
		("Recent 6 Month", date_six_month_back.strftime(date_format)), \
		("Recent Year", date_one_year_back.strftime(date_format)))

	# save_ratio_into_file(fund, from_date, to_date)
	for fund in fund_list:
		# print fund[0]
		for from_date in from_date_list:
			# print from_date[0]
			(_, premium_value_map) = calc_premium_ratio(fund[0], from_date[1], to_date) #TODO, we don't need to retrieve value every time
			for current_premium in (fund[1] - 8, fund[1], fund[1] + 8):
				ratio = 0
				count = 0
				for premium in premium_value_map.keys():
					count += premium_value_map[premium]
					if premium < current_premium:
						ratio += premium_value_map[premium]

				print "%s, %s, %s, %s, %s, %s" % (fund[0], from_date[0], current_premium, count, ratio, float(ratio)/count)