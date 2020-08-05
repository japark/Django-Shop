from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from cart.forms import AddProductForm
from cart.cart import Cart
from member.decorators import login_required
from product.models import Product

# Create your views here.


@require_POST
def add(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	form = AddProductForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		cart.add(product=product,
			quantity=cd['quantity'],
			is_update=cd['is_update']
		)
		return redirect('/cart/')
	return redirect('/product/' + str(product.id) + '/')


def remove(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	cart.remove(product)
	return redirect('/cart/')


@login_required
def detail(request):
	cart = Cart(request)
	for product in cart:
		product['quantity_form'] = AddProductForm(
			initial={'quantity':product['quantity'], 'is_update':True}
		)
	return render(request, 'detail.html', {'cart':cart})