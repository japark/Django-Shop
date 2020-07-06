# Django-Shop
Typical Example of Shopping Mall with Django Engine

After git clone, follow these:

  1) Enter the "Django-Shop" directory.

  2) Make virtual environment:
     - virtualenv venv
     - venv\Scripts\activate (Or "source venv/bin/activate" in Mac)
     - pip install -r requirements.txt

  3) python manage.py migrate

  4) python manage.py createsuperuser
     - Fill in username, email address, password, password(again).

  5) python manage.py runserver
     - Go to 127.0.0.1:8000/admin
     - Login with superuser account made above.
     - You can now control the admin site.

  6) Go to 127.0.0.1:8000

  It's the "Django-Shop" website, which is intended to show you.

This Django-Shop consists of three apps: member, product, and order.


In member.views, note
  1. How FormView and its method form_valid() are used,
  2. How one can approach form data by form.data or form.cleaned_data in form_valid() method, and
  3. How to approach request information when class view is used.  
Only in the method of class view, self.request makes one approach request information.

In member.forms, note how to intervene validity-check of form by inheriting clean() method of forms.Form class.

In member.decorators, note the principle of making decorators and the use of wrap() function inside.  
Also note how they are used(@method_decorator) in the views.py in product and order apps.


In product.views, specially note the harmony of OrderForm (defined in order app, forms.py) and the class view inheriting DetailView.  
Also, a class variable "queryset" is used instead of "model".  
It doesn't matter to use "model" here, but one can apply conditions on look-up table with "queryset".

In product.forms, note the comment-out part.  
This shows it's better to write code, which is implemented after successful validation, in form_valid() method in views.py rather than in clean() method in forms.py.

In product app, DRF(Django Rest Framework) is used in serializers.py and views.py.  
It's a well-known trend to separate the development into two parts: frontend and backend.  
DRF makes it easier to develop API in backend part, thus focus more on the business logic itself.

In product templates, the famous board interface "SummerNote" is used,  
and "humanize" is loaded by {% load humanize %} to make use of a template filter(intcomma) that makes numbers more human-friendly and readable.


In order.views, note
1. Appearance of form_invalid() method, which seems to be called when self.add_error works in forms.py,
2. Introduction of the concept of "transaction",
3. How to transfer arguments, by using get_form_kwargs() method, to the form class allocated to form_class variable, and
4. Use of get_queryset() method.







