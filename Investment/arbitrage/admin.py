from django.contrib import admin


# Register your models here.
from .models import CompanyInfo, Product, ProductType, StructuredFund, MarketData
from .models import InterestRule, DeriveProduct, FixIncomeProduct

admin.site.register(CompanyInfo)
admin.site.register(Product)
admin.site.register(ProductType)
admin.site.register(StructuredFund)
admin.site.register(DeriveProduct)
admin.site.register(FixIncomeProduct)
admin.site.register(InterestRule)