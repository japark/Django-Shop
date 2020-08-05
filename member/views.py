from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.hashers import make_password

from cart.cart import Cart
from member.forms import RegisterForm, LoginForm
from member.models import Member

# Create your views here.


def index(request):
	return render(request, 'index.html', {'email':request.session.get('user')})


class RegisterView(FormView):
	template_name = 'register.html'
	form_class = RegisterForm
	success_url = '/'

	def form_valid(self, form):
		# print(form.cleaned_data)
		member = Member(
			email=form.data.get('email'),
			password=make_password(form.data.get('password')),
			level='user'
		)
		member.save()
		return super().form_valid(form)


class LoginView(FormView):
	template_name = 'login.html'
	form_class = LoginForm
	success_url = '/'

	def form_valid(self, form):
		# self.request.session['user'] = form.email
		self.request.session['user'] = form.data.get('email')
		return super().form_valid(form)


def logout(request):
	cart = Cart(request)
	cart.clear()
	if 'user' in request.session:
		del request.session['user']
	return redirect('/')