from django.shortcuts import render
from django.views.generic import View, TemplateView, CreateView, FormView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from .forms import CheckoutForm, CustomerRegistrationForm, CustomerLoginForm
from .models import *


class EcommMixin(object): #assign a customer to a cart
   def dispatch(self,request, *args, **kwargs):
      cart_id = request.session.get('cart_id')
      if cart_id:
         cart_obj = Cart.objects.get(id=cart_id)
         if request.user.is_authenticated and request.user.customer:
           cart_obj.customer = request.user.customer
           cart_obj.save()
      return super().dispatch(request, *args, **kwargs)

class HomeView(TemplateView, EcommMixin):
   template_name = 'index.html'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['products'] = Product.objects.all().order_by('-id')
      return context

class AllProductsView(TemplateView, EcommMixin):
   template_name = 'categories.html'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['categories'] = Category.objects.all()
      return context

class ProductDetailView(TemplateView):
   template_name = 'productdetail.html'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      url_slug = self.kwargs['slug']
      product = Product.objects.get(slug=url_slug)
      product.view_count += 1
      product.save()
      context['product'] = product
      return context

class AddToCartView(TemplateView, EcommMixin):
   template_name = 'addtocart.html'

   def get_context_data(self, **kwargs):
      context =  super().get_context_data(**kwargs)
      # get product id from requested url
      product_id = self.kwargs['pro_id']
      # get product
      product_obj = Product.objects.get(id=product_id)
      
      # check if cart exists
      cart_id = self.request.session.get('cart_id', None)#get card id from session
      if cart_id:
         cart_obj = Cart.objects.get(id=cart_id)
         this_product_in_cart = cart_obj.cartitem_set.filter(product=product_obj)
         
         # if item already exists in cart
         if this_product_in_cart.exists():
            cartitem = this_product_in_cart.last()
            cartitem.quantity += 1
            cartitem.subtotal += product_obj.selling_price
            cartitem.save()
            cart_obj.total += product_obj.selling_price
            cart_obj.save()
         
         # new item is added in cart
         else:
            cartitem = CartItem.objects.create(
                  cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal = product_obj.selling_price)
            cart_obj.total += product_obj.selling_price
            cart_obj.save()

      else:
         cart_obj = Cart.objects.create(total=0)
         self.request.session['cart_id'] = cart_obj.id
         cartitem = CartItem.objects.create(
               cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal = product_obj.selling_price)
         cart_obj.total += product_obj.selling_price
         cart_obj.save()

      return context
   
class MyCartView(TemplateView, EcommMixin):
   template_name = 'mycart.html'

   def get_context_data(self, **kwargs):      
      context =  super().get_context_data(**kwargs)
      cart_id = self.request.session.get("cart_id", None)
      if cart_id:
         cart = Cart.objects.get(id=cart_id)
      else:
         cart = None
      context['cart'] = cart
      return context

class ManageCartView(View, EcommMixin):
   def get(self, request, *args, **kwargs):
      print("This is manage cart section")
      cp_id = self.kwargs['cp_id']
      action = request.GET.get('action')
      cp_obj = CartItem.objects.get(id=cp_id)
      cart_obj = cp_obj.cart

      if action == 'inc':
         cp_obj.quantity += 1
         cp_obj.subtotal += cp_obj.rate
         cp_obj.save()
         cart_obj.total += cp_obj.rate
         cart_obj.save()
      elif action == 'dcr':
         cp_obj.quantity -= 1
         cp_obj.subtotal -= cp_obj.rate
         cp_obj.save()
         cart_obj.total -= cp_obj.rate
         cart_obj.save()
         if cp_obj.quantity == 0: #if quantity is zero then delete object row
            cp_obj.delete()

      elif action == 'rmv':
         cart_obj.total -= cp_obj.subtotal
         cart_obj.save()
         cp_obj.delete()
      else:
         pass
      return redirect("iSoko:mycart")
   
class EmptyCartView(View, EcommMixin):
   def get(self, request, *args, **kwargs):
      cart_id = request.session.get('cart_id', None)
      if cart_id:
         cart = Cart.objects.get(id=cart_id)
         cart.cartitem_set.all().delete()
         cart.total = 0 
         cart.save()
      return redirect('iSoko:mycart')


class CheckoutView(CreateView, EcommMixin):
   template_name = 'checkout.html'
   form_class = CheckoutForm
   success_url = reverse_lazy('iSoko:home') #redirection url after successful form submission

   def dispatch(self, request, *args, **kwargs):
      user = request.user
      if request.user.is_authenticated and request.user.customer:
         pass
      else:
         return redirect("/login/?next=/checkout/")
      return super().dispatch(request, *args, **kwargs)
   
   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      cart_id = self.request.session.get('cart_id', None)
      if cart_id:
         cart_obj = Cart.objects.get(id=cart_id)
      else:
         cart_obj = None
      context['cart'] = cart_obj
      return context       

   def form_valid(self, form):
      cart_id = self.request.session.get('cart_id')
      if cart_id:#if cart exists
         cart_obj = Cart.objects.get(id=cart_id)
         form.instance.cart = cart_obj
         form.instance.subtotal = cart_obj.total
         form.instance.total = cart_obj.total
         form.instance.discount = 0
         form.instance.order_status = "Order Received"
         del self.request.session["cart_id"]
      else:
         return redirect("iSoko:home")
      return super().form_valid(form)
   
class CustomerRegistration(CreateView):
   template_name = "customerregistration.html"
   form_class = CustomerRegistrationForm
   success_url = reverse_lazy('iSoko:home')

   def form_valid(self, form):
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      email = form.cleaned_data.get('email')
      user = User.objects.create_user(username, email, password)
      form.instance.user = user
      login(self.request, user)
      return super().form_valid(form)
   
   #to overide the success_url variable
   def get_success_url(self):
      if 'next' in self.request.GET:
         next_url = self.request.GET['next']
         return next_url
      else:
         return self.success_url


class CustomerLogoutView(View):
   def get(self, request):
      logout(request)
      return redirect("iSoko:home")

class CustomerLoginView(FormView):
   template_name = "customerlogin.html"
   form_class = CustomerLoginForm
   success_url = reverse_lazy('iSoko:home')

   def form_valid(self, form):
      uname = form.cleaned_data.get('username')
      p_word = form.cleaned_data.get('password')
      user = authenticate(username=uname, password=p_word)
      if user is not None and user.customer:
         login(self.request, user)
      else:
         return render(self.request, self.template_name, 
         {"form": self.form_class, "error":"Invalid username or password"})
      
      return super().form_valid(form)
   
   #to overide the success_url variable
   def get_success_url(self):
      if 'next' in self.request.GET:
         next_url = self.request.GET['next']
         return next_url
      else:
         return self.success_url


class ContactView(TemplateView, EcommMixin):
   template_name = 'contact.html'

class AboutView(TemplateView,EcommMixin):
   template_name = 'about.html'
