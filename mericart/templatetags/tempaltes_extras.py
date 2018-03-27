import string
import random
from django.shortcuts import render
from django.core.paginator import PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.http import *
from django.contrib.auth.models import User
from mericart.forms import *
from django.conf import settings
from shopping.settings import *
from django.db.models import Q
from django import template

register = template.Library()

@register.filter(name='get_cartitemscount')
def get_cartitemscount():
    u = request.user
    p = u.cart_set.filter(purchased = False)
    return p.count()

@register.filter(name='printdemo')
def printdemo():
    return "Thanks"
