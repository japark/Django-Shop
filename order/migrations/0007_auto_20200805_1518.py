# Generated by Django 3.0.8 on 2020-08-05 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20200805_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_count',
            field=models.IntegerField(default=0, verbose_name='주문제품총갯수'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='variety',
            field=models.IntegerField(default=0, verbose_name='주문제품종류수'),
            preserve_default=False,
        ),
    ]
