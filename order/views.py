from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.db import transaction

from datetime import datetime
import math

from rest_framework import generics
from rest_framework import mixins

from cart.cart import Cart

from member.decorators import login_required
from member.models import Member

from order.forms import OrderCreateForm, RegisterForm
from order.models import Order, OrderItem
from order.serializers import OrderSerializer

from product.models import Product

# Create your views here.


class OrderSearchAPI(generics.GenericAPIView, mixins.ListModelMixin):
	serializer_class = OrderSerializer

	def get_queryset(self):
		order_date_from = self.request.query_params.get('date_from')
		if not order_date_from: order_date_from = '0001-01-01'
		order_date_from = datetime.strptime(order_date_from, '%Y-%m-%d')
		order_date_until = self.request.query_params.get('date_until')
		if not order_date_until:
			now_dttm = datetime.now()
			order_date_until = str(now_dttm.year) + '-' + str(now_dttm.month) + '-' + str(now_dttm.day)
		order_date_until += ' 23:59:59'
		order_date_until = datetime.strptime(order_date_until, '%Y-%m-%d %H:%M:%S')
		orders = Order.objects.filter(registered_dttm__gte=order_date_from)
		orders = orders.filter(registered_dttm__lte=order_date_until)

		dates = self.request.query_params.get('register_date')
		querysets = []
		if dates:
			for date in dates.split(','):
				cvt_date = datetime.strptime(date, '%Y-%m-%d')
				querysets.append(orders.filter(
					registered_dttm__year=cvt_date.year,
					registered_dttm__month=cvt_date.month,
					registered_dttm__day=cvt_date.day)
				)
			orders = querysets[0]
			for i in querysets[1:]:
				orders = orders.union(i)

		total_price_from = self.request.query_params.get('total_price_from')
		if not total_price_from: total_price_from = 0
		total_price_to = self.request.query_params.get('total_price_to')
		if not total_price_to: total_price_to = math.inf
		total_price_from = float(total_price_from)
		total_price_to = float(total_price_to)
		querysets = []
		for i in orders:
			total_price = 0
			for j in i.orderitem_set.all():
				total_price += j.price * j.quantity
			if total_price >= total_price_from and total_price <= total_price_to:
				querysets.append(Order.objects.filter(pk=i.pk))
		if querysets:
			orders = querysets[0]
			for i in querysets[1:]:
				orders = orders.union(i)
		else:
			orders = Order.objects.none()

		product_ids = self.request.query_params.get('product')
		if product_ids:
			product_ids = list(map(int, product_ids.split(',')))
			tmp_orders = Order.objects.filter(orderitem__product__id__in=product_ids).distinct()
			orders = orders.intersection(tmp_orders)

		quantity = self.request.query_params.get('quantity')
		if quantity:
			tmp_orders = Order.objects.filter(orderitem__quantity=quantity).distinct()
			orders = orders.intersection(tmp_orders)

		contains = self.request.query_params.get('contains')
		if contains:
			tmp_orders = Order.objects.filter(orderitem__product__name__contains=contains).distinct()
			orders = orders.intersection(tmp_orders)

		price_from = self.request.query_params.get('price_from')
		if not price_from: price_from = 0
		price_to = self.request.query_params.get('price_to')
		if not price_to: price_to = math.inf
		tmp_orders = Order.objects.filter(orderitem__price__gte=price_from)
		tmp_orders = tmp_orders.filter(orderitem__price__lte=price_to)
		orders = orders.intersection(tmp_orders)

		total_count = self.request.query_params.get('total_count')
		if total_count:
			querysets = []
			for i in orders:
				cnt = 0
				for j in i.orderitem_set.all():
					cnt += j.quantity
				if cnt == int(total_count):
					order = Order.objects.filter(pk=i.pk)
					querysets.append(order)
			if querysets:
				orders = querysets[0]
				for i in querysets[1:]:
					orders = orders.union(i)
			else:
				orders = Order.objects.none()

		domain = self.request.query_params.get('domain')	
		tmp_orders = Order.objects.filter(user__email__contains=domain)
		orders = orders.intersection(tmp_orders)

		join_date_from = self.request.query_params.get('join_from')
		if not join_date_from: join_date_from = '0001-01-01'
		join_date_until = self.request.query_params.get('join_until')
		if not join_date_until:
			now_dttm = datetime.now()
			join_date_until = str(now_dttm.year) + '-' + str(now_dttm.month) + '-' + str(now_dttm.day)
		join_date_until += ' 23:59:59'
		join_date_from = datetime.strptime(join_date_from, '%Y-%m-%d')
		join_date_until = datetime.strptime(join_date_until, '%Y-%m-%d %H:%M:%S')
		tmp_orders = Order.objects.filter(user__registered_dttm__gte=join_date_from)
		tmp_orders = tmp_orders.filter(user__registered_dttm__lte=join_date_until)
		orders = orders.intersection(tmp_orders)

		return orders.all()

	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)


def order_search(request):
	if request.method == 'POST':
		data = request.POST['data']
		if data:
			data = data.split(',')
			ordering = request.POST.get('ordering')
			if not ordering: ordering = '-id'
			orders = Order.objects.filter(id__in=data).order_by(ordering, '-id')
			page = request.POST.get('page')
			if not page: page = 1
			paginator = Paginator(orders, 5)
			boards = paginator.get_page(page)
			return render(request, 'order_search.html', {'object_list':boards})
	return render(request, 'order_search.html', {})


@login_required
def order_create(request):
	cart = Cart(request)
	if request.method == 'POST':
		form = OrderCreateForm(request.POST)
		if form.is_valid():
			if len(cart) > 0:
				with transaction.atomic():
					email = form.cleaned_data.get('email')
					user = Member.objects.get(email=email)
					order = Order(user=user)
					order.save()
					total_price = 0
					total_count = 0
					variety = 0
					for item in cart:
						product = item['product']
						variety += 1
						quantity = item['quantity']
						total_count += quantity
						price = item['price']
						total_price += price * quantity
						OrderItem.objects.create(
							order=order,
							product=product,
							price=price,
							quantity=quantity
						)
						product.stock -= quantity
						product.save()
					order.total_price = total_price
					order.variety = variety
					order.total_count = total_count
					order.save()
				cart.clear()
				return render(request, 'order_created.html', {'order':order})
	return redirect('/cart/')


@method_decorator(login_required, name='dispatch')
class OrderCreate(FormView):
	form_class = RegisterForm
	success_url = '/product/'

	def form_valid(self, form):
		with transaction.atomic():
			product = Product.objects.get(pk=form.data.get('product'))
			order = Order(
				quantity=form.data.get('quantity'),
				product=product,
				user=Member.objects.get(email=self.request.session.get('user'))
			)
			order.save()
			product.stock -= int(form.data.get('quantity'))
			product.save()
		return super().form_valid(form)

	def form_invalid(self, form):
		# return redirect('/product/'+ str(form.product.id))
		return redirect('/product/'+ str(form.data.get('product')))

	def get_form_kwargs(self, **kwargs):
		kw = super().get_form_kwargs(**kwargs)
		kw.update({
			'request': self.request
		})
		return kw


@method_decorator(login_required, name='dispatch')
class OrderList(ListView):
	# model = Order
	template_name = 'order.html'
	# context_object_name = 'order_list'

	def get_queryset(self, **kwargs):
		queryset = Order.objects.filter(user__email=self.request.session.get('user'))
		return queryset