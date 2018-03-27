import string
import random
from django.shortcuts import render
from django.core.paginator import PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from mericart.models import *
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.http import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.contrib.auth.models import User
from mericart.forms import *
from django.conf import settings
from shopping.settings import *
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib import messages
from django.core.exceptions import *
from django.core.urlresolvers import reverse
from django.template.loader import get_template
from django.template import Context
from django.template.loader import render_to_string

# Create your views here.

def search_view(request):
    if request.method == 'POST':
        q = request.POST.get('q')
        p = Product.objects.filter(Q(name__icontains = q)).order_by('name')
        c = Category.objects.all().order_by('category_name')
        b = Brand.objects.all().order_by('brand').order_by('brand')
        return render(request, 'mericart/home.html',{'pro':p,'cat' : c,'bra':b})
    return HttpResponseRedirect('/home/')

def search_b_view(request, cid = None):
    p = Product.objects.filter(Q(brand__id = cid)).order_by('name')
    c = Category.objects.all().order_by('category_name')
    b = Brand.objects.all().order_by('brand').order_by('brand')
    return render(request, 'mericart/home.html',{'pro':p,'cat' : c,'bra':b})
    
def search_c_view(request, cid = None):
    p = Product.objects.filter(Q(category__id = cid)).order_by('name')
    c = Category.objects.all().order_by('category_name')
    b = Brand.objects.all().order_by('brand').order_by('brand')
    return render(request, 'mericart/home.html',{'pro':p,'cat' : c,'bra':b})

def index_view(request):
    p = Product.objects.all()
    c = Category.objects.all().order_by('category_name')
    b = Brand.objects.all().order_by('brand').order_by('brand')
    return render(request, 'mericart/home.html', {'pro': p,'cat' : c,'bra':b})
    

def register_view(request):
    if request.method == 'POST':
        fn = request.POST.get('firstname')
        ln = request.POST.get('lastname')
        em = request.POST.get('email')
        un = request.POST.get('username')
        ps = request.POST.get('password')
        gn = request.POST.get('gender')
        mb = request.POST.get('phno')
        ad = request.POST.get('add')
        cn = request.POST.get('country')
        st = request.POST.get('state')
        ct = request.POST.get('city')
        pin = request.POST.get('pin_code')
        user = User(username = un, first_name = fn, last_name = ln, password = ps, email = em)
        user.save()
        user = User.objects.get(username=un)
        user.set_password(ps)
        user.save()
        pro = UserProfile(gender=gn, phone_number=mb, address = ad, country = cn, state = st, city = ct, pin_code = pin, user=user)
        pro.save()
        text = 'Thank You for registering to our Web site. http://' + request.get_host() + '/login/ Click Here to Login to MERI CART Website. Hope you will enjoy our service.'
        email = EmailMessage('Registration', text, 'lakshmanraja209@gmail.com', [em])
        email.send()
        return HttpResponseRedirect('/login/')
    return render(request, 'mericart/registration.html')

def reset_view(request):
    return render(request,'mericart/reset.html')


def loginview(request):
    msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/home/')
            else:
                msg = username + ' account has been disabled.'
                return render(request, 'mericart/Login_Page.html', {'message': msg})
        else:
            msg = 'Invalid Username and Password'
    return render(request,'mericart/Login_Page.html',{'message': msg})


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def reset(request):
    return password_reset(request, template_name='mericart/reset.html',
        email_template_name = 'mericart/reset_email.html',
        subject_template_name = 'mericart/reset_subject.txt',
        post_reset_redirect = reverse('success'))


def reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request, template_name='mericart/reset_confirm.html',
        uidb64=uidb64, token=token, post_reset_redirect=reverse('success'))

@login_required(login_url='/login/')
def addcart_view(request, pid=None):
    msg = ""
    u = request.user
    p = Product.objects.get(pk = pid)
    e = Cart.objects.filter(user=u,product=p,purchased=False)
    if e:
        p = Product.objects.all()
        c = Category.objects.all().order_by('category_name')
        b = Brand.objects.all().order_by('brand').order_by('brand')
        msg = "This item is alreay present in the cart"
        return render(request, 'mericart/home.html', {'pro': p,'cat' : c,'bra':b,'msg':msg})
    else:
        tot = float(p.price)
        c=Cart(user=u,product=p,total_cost=tot)
        c.save()
        return HttpResponseRedirect('/home/')

def preview_view(request, pid=None):
    u = request.user
    p = Product.objects.get(pk = pid)
    c = Category.objects.all().order_by('category_name')
    b = Brand.objects.all().order_by('brand')
    return render(request,'mericart/preview.html',{'pro':p,'cat':c,'bra':b})


def success(request):
  return render(request, "mericart/success.html")

@login_required(login_url='/login/')
def cart_buy_view(request):
    u = request.user
    p = u.cart_set.filter(purchased = False)
    pt = u.cart_set.filter(purchased = True)
    c = Category.objects.all().order_by('category_name')
    sum = 0.0
    for i in p:
        sum = sum + float(i.total_cost)
    b = Brand.objects.all().order_by('brand')
    return render(request, 'mericart/Cart.html', {'pro':p,'cat':c,'tot':sum,'prot':pt,'bra':b})


@login_required(login_url='/login/')
def preview_add_view(request, pid=None, cid=None):
    u = request.user
    p = Product.objects.get(pk = pid)
    tot = float(p.price) * float(cid)
    cd=int(cid)
    c=Cart(user=u,product=p,total_no_product=cd,total_cost=tot)
    c.save()
    p = Product.objects.get(pk = pid)
    c = Category.objects.all().order_by('category_name')
    return HttpResponseRedirect('/preview/' + pid)

def shipping_view(request):
    u = request.user
    if request.method == 'POST':
        street = request.POST.get('street')
        lm = request.POST.get('landmark')
        cn = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        zp = request.POST.get('zip')
        mb = request.POST.get('mobile')
        amb = request.POST.get('altmobile')
        try:
            s = Shipping.objects.get(user = u)
            s.street_add = street
            s.land_mark = lm
            s.country = cn
            s.state = state
            s.city = city
            s.postel_pin = zp
            s.mobile_no = mb
            s.alternative_no = amb
            s.save()
        except ObjectDoesNotExist:
            s = Shipping(user = u, street_add = street, land_mark = lm, country = cn, state = state, city = city, postel_pin = zp, mobile_no = mb, alternative_no = amb)
            s.save()
        return HttpResponseRedirect('/pay/')
    p = Product.objects.all()
    c = Category.objects.all().order_by('category_name')
    b = Brand.objects.all().order_by('brand')
    ct = u.cart_set.filter(purchased = False)
    sum = 0.0
    for i in ct:
        sum = sum + float(i.total_cost)
    return render(request, 'mericart/shipping.html',{'pro':p,'cat':c,'bra':b,'car':ct, 'tot':sum})

	
def pay_view(request):
    u = request.user    
    c = Category.objects.all().order_by('category_name')
    p = Product.objects.all()
    b = Brand.objects.all().order_by('brand')
    ct = u.cart_set.filter(purchased = False)
    car = ct
    sh = Shipping.objects.get(user = u)
    sum = 0.0
    for i in ct:
        sum = sum + float(i.total_cost)
    if request.method == 'POST':
        order = generator()
        payment_type = request.POST.get('pay_type')
        card_no = request.POST.get('card')
        cvv = request.POST.get('cvv')
        expiry = request.POST.get('expiry')
        
        if payment_type == "1":
            payment_type = "Cash on Delivery"
        if payment_type == "2":
            payment_type = "Debit Card"
        if payment_type == "3":
            payment_type = "Credit Card"
    
        if payment_type == "Cash on Delivery":
            pay = Pay(order_no = order, payment_type = payment_type)
        else:
            pay = Pay(order_no = order, payment_type = payment_type, card_no = card_no, cvv = cvv, expiry = expiry)
        pay.save()
        pay = Pay.objects.get(order_no = order)
        sh = Shipping.objects.get(user = u)
        ship = sh.street_add + " " + sh.land_mark + " " + sh.country + " " + sh.state + " " + sh.city + " " + str(sh.postel_pin) + " " + str(sh.mobile_no) + " " + str(sh.alternative_no) 
        for i in ct:
            bill = Billing(user = u, order_no = order, product_name = i.product.name, product_code = i.product.product_code, quantity = i.total_no_product, single_price = i.product.price, total_price = i.total_cost,shipping_address = ship,pay = pay, status = "Approved")
            bill.save()
            i.purchased = True
            i.save()
            pro = Product.objects.get(id=i.product.id)
            stock = Stock.objects.get(product = pro)
            stock.stock_no = stock.stock_no - i.total_no_product
            stock.save()
        msg_html = render_to_string('mericart/email.html', {'order': order,'car':car,'tot':sum, 'sh':sh})
        send_mail('Thank You for your Order', 'Thank You for your Order' ,'palsbca.pb@gmail.com',[u.email],html_message=msg_html)
        return HttpResponseRedirect('/thank_you/' + order)
    return render(request, 'mericart/pay.html', {'cat':c,'pro':p,'bra':b, 'car':ct, 'tot':sum, 'ship':sh})

def generator(size=11, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range (size))

def delete_view(request, cid = None):
    c = Cart.objects.get(pk = cid)
    c.delete()
    return HttpResponseRedirect('/cart_buy/')

def thank_you_view(request, cid = None):
    u = request.user    
    c = Category.objects.all().order_by('category_name')
    p = Product.objects.all()
    b = Brand.objects.all().order_by('brand')
    bill = Billing.objects.filter(order_no = cid)
    sum = 0.0
    for i in bill:
        sum = sum + float(i.total_price)
    ship = Shipping.objects.get(user = u)
    return render(request, 'mericart/thank_you.html', {'cat':c,'pro':p,'bra':b, 'bill':bill, 'tot':sum, 'ship':ship, 'ord':cid})
    
def my_order_view(request):
    u = request.user    
    c = Category.objects.all().order_by('category_name')
    p = Product.objects.all()
    b = Brand.objects.all().order_by('brand')
    bill = Billing.objects.filter(user = u).order_by('order_date')
    return render(request, 'mericart/my_order.html', {'cat':c,'pro':p,'bra':b, 'bill':bill})
