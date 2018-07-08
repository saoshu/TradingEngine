from django.db import models

# Create your models here.
class CompanyInfo(models.Model):
	company_name = models.CharField(max_length=30)
	company_url = models.CharField(max_length=100)

	def __str__(self):
		return self.company_name

class ProductType(models.Model):
	type_name = models.CharField(max_length=20)
	type_code = models.CharField(max_length=10)

	def __str__(self):
		return self.type_name

class Product(models.Model):
	product_name = models.CharField(max_length=30)
	product_code = models.CharField(max_length=20)
	product_code.primary_key = True
	tradable = models.BooleanField(default=False)
	issue_company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE)
	product_type = models.ForeignKey(ProductType)#TODO on_delete values?

	def __str__(self):
		return self.product_name

class InterestRule(models.Model):
	rule_name = models.CharField(max_length=30)
	rule = models.CharField(max_length=100)#formula

class FixIncomeProduct(models.Model):
	product_code = models.ForeignKey(Product, on_delete=models.CASCADE)

	#initial par value
	#
	interest_rate = models.FloatField(default=0.0)
	interest_rate_rule = models.ForeignKey(InterestRule, on_delete=models.PROTECT)
	#TODO more attributes for FixIncomeProudct

class DeriveProduct(models.Model):
	product_code = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="derive_products")
	underlier_product_code = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="underlier_products")
	#TODO 
	# Add derivative rules

class StructuredFund(models.Model):
	base_product_code = models.ForeignKey(Product, on_delete=models.CASCADE)
	leg_a = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="structured_leg_a")
	leg_b = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="structured_leg_b")

	ratio_a = models.IntegerField(default=1)
	ratio_b = models.IntegerField(default=1)

	def __str__(self):
		return str(self.base_product_code)
		# return Product.objects.get(pk=self.base_product_code)

class MarketData(models.Model):
	product_code = models.ForeignKey(Product)

	current_date = models.DateField()
	current_time = models.TimeField()

	#valid attributes for tradable product only
	current_px = models.FloatField(default=0.0)
	close_px = models.FloatField(default=0.0)
	premium_rate = models.FloatField(default=0.0)

	#valid attributes for fixed income products who have face value, etc
	cur_face_value = models.FloatField(default=1.0)
	cum_face_value = models.FloatField(default=1.0)