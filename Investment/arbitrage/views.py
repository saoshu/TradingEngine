from django.shortcuts import render

from .models import *

# Create your views here.
def index(request):
	structured_fund_list = StructuredFund.objects.all()
	context = {'structured_fund_list':structured_fund_list}
	return render(request, "arbitrage/index.html", context)

def test(request):
	context = {}
	return render(request, "arbitrage/test.html", context)
	
def reload(request):
	# import os
	# print (os.getcwd())
	structured_fund_type = ProductType.objects.get(type_name='股票基金')
	a_fund_type = ProductType.objects.get(type_name='分级A')
	b_fund_type = ProductType.objects.get(type_name='分级B')
	import csv
	with open("arbitrage/structured_fund_list.csv", newline='') as f:
		reader = csv.DictReader(f)
		for row in reader:
			company = CompanyInfo.objects.get(company_name=row['基金公司'])
			base_product = Product(product_code=row['母基代码'],product_name=row['母基名称'], issue_company=company, product_type=structured_fund_type)
			a_product = Product(product_code=row['A基代码'],product_name=row['A基名称'], issue_company=company, product_type=a_fund_type)
			b_product = Product(product_code=row['B基代码'],product_name=row['B基名称'], issue_company=company, product_type=b_fund_type)

			base_product.save()
			a_product.save()
			b_product.save()

			ratio = row['A:B'].split(":")
			structured_fund = StructuredFund(base_product_code=base_product, 
											leg_a=a_product, leg_b=b_product,
											ratio_a=ratio[0], ratio_b=ratio[1])
			structured_fund.save()

# def dump_structured_fund(request):
# 	import csv
# 	products = Product.objects.all()
# 	for p in products:
		
# 	with open("structured_fund_dump.csv", 'w', newline="") as f:
# 		writer = csv.writer(f)
# 		writer.writerows(structured_fund_list)