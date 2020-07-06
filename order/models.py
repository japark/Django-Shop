from django.db import models

# Create your models here.


class Order(models.Model):
	user = models.ForeignKey("member.Member", on_delete=models.CASCADE, verbose_name="주문자")
	product = models.ForeignKey("product.Product", on_delete=models.CASCADE, verbose_name="상품")
	quantity = models.IntegerField(verbose_name="수량")
	registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name="주문날짜")

	def __str__(self):
		return str(self.user) + " " + str(self.product)

	class Meta:
		db_table = 'Order'
		verbose_name = '주문'
		verbose_name_plural = '주문내역'