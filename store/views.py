import random
from django.http import JsonResponse
import django
from django.contrib.auth.models import User
from store.models import Customerdetails, Cart, Category, Order, Product, payments, staff, Feedback, Orderdetail, \
    contact, ProductReview, Adds
from django.shortcuts import redirect, render, get_object_or_404
from .forms import RegistrationForm, AddressForm, addstockform, dailreportform, addproductform, LoginForm, \
    StaffUpdateorderForm, ReviewAdd
from django.contrib import messages
from django.views import View
from django.db.models import Max, Min, Count, Avg
import decimal
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator  # for Class Based Views
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, \
    PasswordResetForm, SetPasswordForm
from django.db import models
from django.db.models import fields
from django.forms import widgets
from django.forms.fields import CharField
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
def firstone(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobno = request.POST['mobno']
        message = request.POST['message']
        contact(name=name, email=email, mobno=mobno, message=message).save()
    context = {
        'addd': Adds.objects.all()
    }
    return render(request, 'firstone.html', context)


def new(request):
    return render(request, 'new.html')


def home(request):
    categories = Category.objects.filter(is_active=True, is_featured=True)[:3]
    products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    context = {
        'categories': categories,
        'products': products,
    }

    # for x in categories:
    #     print(x)
    for y in products:
        print(y.title, '------->', y.product_image)
    return render(request, 'store/index.html', context)


def detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.exclude(id=product.id).filter(is_active=True, category=product.category)

    # Fetch reviews

    context = {
        'product': product,
        'related_products': related_products,

    }
    return render(request, 'store/detail.html', context)


def all_categories(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, 'store/categories.html', {'categories': categories})


def category_products(request, slug):
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(is_active=True, category=category)
    categories = Category.objects.filter(is_active=True)
    context = {
        'category': category,
        'products': products,
        'categories': categories,
    }

    print(category)
    print(products)
    print(categories)
    return render(request, 'store/category_products.html', context)


def customeraddfeedback(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        msg = request.POST['message']
        Feedback(name=name, email=email, msg=msg).save()
    return render(request, 'store/addfeedback.html')


# Authentication Starts Here

class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        print(form)
        if form.is_valid():
            messages.success(request, "Congratulations! Registration Successful!")
            form.save()
        return render(request, 'account/register.html', {'form': form})


class LoginView(View):
    template_name = 'account/login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        print(form)
        print('ggggg')
        print(request.POST['username'])
        print(request.POST['password'])
        if not form.is_valid():
            user = authenticate(
                username=request.POST['username'],
                password=request.POST['password'],
            )

            print('user--->', user)

            if user is not None:
                if user.is_staff:
                    login(request, user)
                return redirect('store:profile')
        message = 'Login failed!'
        # return redirect('store:profile')
        return render(request, 'account/login.html')


@login_required
def profile(request):
    addresses = Customerdetails.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user).order_by('-user_id')
    return render(request, 'account/profile.html', {'addresses': addresses, 'orders': orders})


@method_decorator(login_required, name='dispatch')
class AddressView(View):
    def get(self, request):
        form = AddressForm()
        return render(request, 'account/add_address.html', {'form': form})

    def post(self, request):
        form = AddressForm(request.POST)
        print('-------')
        if not form.is_valid():
            print(request.POST['locality'])
            user = request.user
            locality = request.POST['locality']
            city = request.POST['city']
            email = request.POST['email']
            mobno = request.POST['mobno']
            rationcardno = request.POST['rationcardno']
            rationcardphoto = request.FILES['rationcardphoto']
            reg = Customerdetails(user=user, locality=locality, city=city, mobno=mobno, email=email,
                                  rationcardno=rationcardno,
                                  rationcardphoto=rationcardphoto)
            reg.save()
            messages.success(request, "New Address Added Successfully.")

        return redirect('store:profile')


@login_required
def remove_address(request, id):
    a = get_object_or_404(Customerdetails, user=request.user, id=id)
    a.delete()
    messages.success(request, "Address removed.")
    return redirect('store:profile')


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)

    # Check whether the Product is alread in Cart or Not
    item_already_in_cart = Cart.objects.filter(product=product_id, user=user)
    if item_already_in_cart:
        cp = get_object_or_404(Cart, product=product_id, user=user)
        cp.quantity += 1
        cp.save()
    else:
        Cart(user=user, product=product).save()

    return redirect('store:cart')


@login_required
def cart(request):
    user = request.user
    cart_products = Cart.objects.filter(user=user)

    # Display Total on Cart Page
    amount = decimal.Decimal(0)
    shipping_amount = decimal.Decimal(10)
    # using list comprehension to calculate total amount based on quantity and shipping
    cp = [p for p in Cart.objects.all() if p.user == user]
    if cp:
        for p in cp:
            temp_amount = (p.quantity * p.product.price)
            amount += temp_amount

    # Customer Addresses
    addresses = Customerdetails.objects.filter(user=user)

    context = {
        'cart_products': cart_products,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'total_amount': amount + shipping_amount,
        'addresses': addresses,
    }
    return render(request, 'store/cart.html', context)


@login_required
def remove_cart(request, cart_id):
    if request.method == 'GET':
        c = get_object_or_404(Cart, id=cart_id)
        c.delete()
        messages.success(request, "Product removed from Cart.")
    return redirect('store:cart')


@login_required
def plus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        cp.quantity += 1
        if cp.quantity >= cp.product.productStock:
            cp.quantity -= 1
        cp.save()
    return redirect('store:cart')


@login_required
def minus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        # Remove the Product if the quantity is already 1
        if cp.quantity == 1:
            cp.delete()
        else:
            cp.quantity -= 1
            cp.save()
    return redirect('store:cart')


@login_required
def checkout(request):
    user = request.user
    address_id = request.GET.get('address')

    address = get_object_or_404(Customerdetails, id=address_id)
    cp = [p for p in Cart.objects.all() if p.user == user]

    total = decimal.Decimal(0)
    gstAmount = decimal.Decimal(10)
    orderId = random.randint(111111, 999999)
    for cart in cp:
        total += (cart.quantity * cart.product.price)
    finalTotalWithGst = total + gstAmount

    orders = Order(user=user, address=address, subtotal=total, gst=gstAmount, order_id=orderId,
                   total=finalTotalWithGst).save()
    print('==================================', orders)
    print('total--->', finalTotalWithGst)
    print(Order.objects.latest('id'))

    amount = decimal.Decimal(0)
    if cp:
        for p in cp:
            print('ppp', p.product)
            Orderdetail(order=Order.objects.latest('id'), product=p.product.id, product_name=p.product,
                        quantity=p.quantity,
                        price=p.product.price).save()
    return redirect('store:orders')


@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-user_id')

    return render(request, 'store/orders.html', {'orders': orders})


def orderdetail(request, id):
    orderitems = Orderdetail.objects.filter(order=id)

    orders = Orderdetail.objects.raw("SELECT * FROM store_orderdetail")

    return render(request, 'store/orderview.html', {'orderitems': orderitems, 'orders': orders})


def shop(request):
    return render(request, 'store/shop.html')


def test(request):
    return render(request, 'store/test.html')


def paymentview(request):
    if request.method == 'POST':
        cardname = request.POST['cardname']
        cardno = request.POST['cardno']

        amount = request.POST['amount']
        payments(name=cardname, cardno=cardno, amount=amount).save()

    return render(request, 'store/payment.html')


def inform(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        email = request.POST.get('email')
        send_mail(subject, message, settings.EMAIL_HOST_USER,
                  [email], fail_silently=False)
        return render(request, 'staff/email_sent.html', {'email': email})
    return render(request, 'staff/sendmail.html')


# staff
# def stafflogin(request):
#     # staffId = request.form['staff_id']
#
#     # print('$$$$$$', staffId)
#     # staffdetails = staff.objects.get(id=staff_id, name=name, password=password)
#     #
#     return render(request, 'staff/stafflogin.html')


def staffloginaction(request):
    if request.method == 'POST':

        staffId = request.POST['staff_id']
        name = request.POST['name']
        password = request.POST['password']

        print('$$$$$', staffId)
        print('$$$$$', name)
        print('$$$$$', password)

        staffdetails = staff.objects.get(staff_id=staffId, name=name, password=password)


        if staffdetails:
            return render(request, 'staff/staffhome.html')

        else:
            messages.error(request,'not a staff')
        return render(request,'staff/stafflogin.html')

    return render(request, 'staff/stafflogin.html')


def staffhome(request):
    return render(request, 'staff/staffhome.html')


def staffviewrationcard(request):
    context = {
        'ration': Customerdetails.objects.all()
    }
    return render(request, 'staff/viewrationcard.html', context)


def addproducts(request):
    context = {}

    print('%%%%%%', request.FILES)
    print('%%%%%%', request.POST)
    # create object of form
    form = addproductform(request.POST or None, request.FILES or None)

    print('&&&&&', form)

    # check if form data is valid
    if form.is_valid():
        # save the form data to model
        form.save()

    context['form'] = form
    return render(request, "staff/addproduct.html", context)


def stafftakeorder(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')

    # for x in orders:
    #
    #     print('*********************', x.order_id)

    return render(request, 'staff/takeorder.html', {'orders': orders})


def staffupdateorder(request, id):
    print(id)
    if request.method == "POST":
        form = StaffUpdateorderForm(request.POST)
        if form.is_valid():
            form.user = request.user
            order = Order.objects.get(id=id)
            status = request.POST['status']
            order.status = status
            order.save()
        else:
            messages.success(request, 'error')
    else:
        form = StaffUpdateorderForm()

    return render(request, 'staff/updateorder.html', {'form': form})


def staffviewcustomer(request):
    context = {
        'customerdetails': Customerdetails.objects.all(),
    }

    return render(request, 'staff/viewcustomerdetail.html', context)


def staffaddreport(request):
    context = {}

    # create object of form
    form = dailreportform(request.POST or None, request.FILES or None)

    # check if form data is valid
    if form.is_valid():
        # save the form data to model
        form.save()

    context['form'] = form
    return render(request, 'staff/addreport.html', context)


def staffaddstock(request):
    context = {}

    # create object of form
    form = addstockform(request.POST, request.FILES)

    # check if form data is valid
    if form.is_valid():
        # save the form data to model
        form.save()

    context['form'] = form
    return render(request, 'staff/addstock.html', context)


def staffvieworderdetails(request, id):
    all_orders = Orderdetail.objects.filter(order=id)

    orders = Orderdetail.objects.raw("SELECT * FROM store_orderdetail")
    return render(request, 'staff/view orderdetails.html', {'all_orders': all_orders, 'orders': orders})


def staffviewfeedback(request):
    context = {
        'feedbacks': Feedback.objects.all()
    }
    return render(request, 'staff/viewfeedback.html', context)


def staffviewcontact(request):
    context = {
        'contacts': contact.objects.all()
    }
    return render(request, 'staff/viewcontact.html', context)


def getsubseedycat(request):
    cat = Category.objects.filter(choice='Subseedy')
    print(cat)
    if cat:
        return render(request, 'store/subseedyproduct.html', {'cat': cat})

    # caat1=Category.objects.filter(choice='NoSubseedy')


def getnosubseedycat(request):
    cati = Category.objects.filter(choice='Nosubseedy')
    print(cati)
    if cati:
        return render(request, 'store/nosubseedyproduct.html', {'cati': cati})


def customerviewdetails(request):
    det = Customerdetails.objects.filter(user=request.user)
    return render(request, 'store/details.html', {'det': det})


# Save Review
def save_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user
    review = ProductReview.objects.create(
        user=user,
        product=product,
        review_text=request.POST['review_text'],
        review_rating=request.POST['review_rating'],
    )
    data = {
        'user': user.username,
        'review_text': request.POST['review_text'],
        'review_rating': request.POST['review_rating']
    }

    # Fetch avg rating for reviews
    avg_reviews = ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
    # End

    return JsonResponse({'bool': True, 'data': data, 'avg_reviews': avg_reviews})


def customeraddreview(request):
    context = {}

    # create object of form
    form = ReviewAdd(request.POST or None, request.FILES or None)

    # check if form data is valid
    if form.is_valid():
        # save the form data to model
        form.save()

    context['form'] = form
    return render(request, 'store/addreview.html', context)


def staffviewreview(request):
    rev=ProductReview.objects.all()
    return render(request, 'staff/viewreview.html',{'rev':rev})
