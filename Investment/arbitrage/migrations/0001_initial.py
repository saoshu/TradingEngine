# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-03 06:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=30)),
                ('company_url', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DeriveProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='FixIncomeProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('par_value', models.FloatField(default=1.0)),
                ('interest_rate', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='InterestRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule_name', models.CharField(max_length=30)),
                ('rule', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MarketData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_date', models.DateField()),
                ('current_time', models.TimeField()),
                ('current_px', models.FloatField(default=0.0)),
                ('close_px', models.FloatField(default=0.0)),
                ('premium_rate', models.FloatField(default=0.0)),
                ('cur_face_value', models.FloatField(default=1.0)),
                ('cum_face_value', models.FloatField(default=1.0)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_name', models.CharField(max_length=30)),
                ('product_code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('tradable', models.BooleanField(default=False)),
                ('issue_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arbitrage.CompanyInfo')),
            ],
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=20)),
                ('type_code', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='StructuredFund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ratio_a', models.IntegerField(default=1)),
                ('ratio_b', models.IntegerField(default=1)),
                ('base_product_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arbitrage.Product')),
                ('leg_a', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='structured_leg_a', to='arbitrage.Product')),
                ('leg_b', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='structured_leg_b', to='arbitrage.Product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arbitrage.ProductType'),
        ),
        migrations.AddField(
            model_name='marketdata',
            name='product_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arbitrage.Product'),
        ),
        migrations.AddField(
            model_name='fixincomeproduct',
            name='interest_rate_rule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='arbitrage.InterestRule'),
        ),
        migrations.AddField(
            model_name='fixincomeproduct',
            name='product_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arbitrage.Product'),
        ),
        migrations.AddField(
            model_name='deriveproduct',
            name='product_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='derive_products', to='arbitrage.Product'),
        ),
        migrations.AddField(
            model_name='deriveproduct',
            name='underlier_product_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='underlier_products', to='arbitrage.Product'),
        ),
    ]
