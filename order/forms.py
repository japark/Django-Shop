from django import forms
# from django.db import transaction

from member.models import Member
from order.models import Order
from product.models import Product


class OrderCreateForm(forms.Form):
    email = forms.CharField(
		label='이메일'
	)


class RegisterForm(forms.Form):
	def __init__(self, request, *arg, **kwargs):
		super().__init__(*arg, **kwargs)
		self.request = request

	quantity = forms.IntegerField(
		error_messages={
			'required':'수량을 입력하세요.'
		}, label='수량'
	)
	product = forms.IntegerField(
		error_messages={
			'required':'상품을 입력하세요.'
		}, label='상품', widget=forms.HiddenInput
	)

	def clean(self):
		cleaned_data = super().clean()
		quantity = cleaned_data.get('quantity')
		product = Product.objects.get(pk=cleaned_data.get('product'))
		# member = Member.objects.get(email=self.request.session.get('user'))

		# if quantity and product and member:
		# 	# Transaction! This part is moved to views.py.
		# 	with transaction.atomic():
		# 		order = Order(
		# 			quantity=quantity,
		# 			product=product,
		# 			user=member
		# 		)
		# 		order.save()
		# 		product.stock -= quantity
		# 		product.save()
		# else:
		# 	self.product = product
		# 	self.add_error('quantity', "수량을 입력하세요.")

		if not (quantity and product):
			self.add_error('quantity', "수량을 입력하세요.")
