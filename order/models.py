from django.db import models

from product.models import Product

# Create your models here.


class Order(models.Model):
	user = models.ForeignKey("member.Member", on_delete=models.CASCADE, verbose_name="주문자")
	total_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
	variety = models.IntegerField(verbose_name="주문제품종류수", default=0)
	total_count = models.IntegerField(verbose_name="주문제품총갯수", default=0)
	registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name="주문날짜")

	def __str__(self):
		return str(self.user) + " " + str(self.registered_dttm)

	class Meta:
		db_table = 'Order'
		verbose_name = '주문'
		verbose_name_plural = '주문내역'


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="주문")
	product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="상품")
	price = models.DecimalField(max_digits=10, decimal_places=0)
	quantity = models.IntegerField(verbose_name="수량")

	def __str__(self):
		return self.product.name

	class Meta:
		db_table = 'OrderItem'
		verbose_name = '주문상품'
		verbose_name_plural = '주문상품목록'