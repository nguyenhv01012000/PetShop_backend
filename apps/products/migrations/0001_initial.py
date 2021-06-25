# Generated by Django 3.1.7 on 2021-06-24 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cateName', models.CharField(default='SOME STRING', max_length=140)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productName', models.TextField(blank=True, null=True)),
                ('productSale', models.IntegerField(default=0)),
                ('productSold', models.IntegerField(default=0)),
                ('productDate', models.DateTimeField(auto_now=True)),
                ('productPrice', models.IntegerField(default=0)),
                ('productCate', models.TextField(blank=True, null=True)),
                ('productColor', models.JSONField(null=True)),
                ('productDes', models.TextField(blank=True, null=True)),
                ('productVote', models.JSONField(null=True)),
                ('productFeature', models.JSONField(null=True)),
                ('productImg', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='products.category')),
            ],
        ),
    ]
