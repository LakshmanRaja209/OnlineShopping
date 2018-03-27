try:
    from django.conf.urls import patterns, include, url
except ImportError:
    from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'shopping.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/', 'mericart.views.index_view', name='Home'),
    url(r'^login/$', 'mericart.views.loginview', name='Login page'),
    url(r'^register/$', 'mericart.views.register_view', name='Register page'),
                       
    # logout
    url(r'^logout/$', 'mericart.views.logout_view', name='Logout'),

    # reset Password
    url(r'^reset/$', 'mericart.views.reset_view', name='reset password'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$','mericart.views.reset_confirm', name='password_reset_confirm'),
    url(r'^ChangePassword/$', 'mericart.views.reset', name='reset'),
    url(r'^success/$', 'mericart.views.success', name='success'),

    # add to cart
    url(r'^add_cart/(?P<pid>\d+)$','mericart.views.addcart_view',name='Add Cart'),

    # Preview Product
    url(r'^preview/(?P<pid>\d+)$','mericart.views.preview_view',name='Preview Product'),

    #Preview Add cart
    url(r'^preview/(?P<pid>\d+)/(?P<cid>\d+)/$','mericart.views.preview_add_view',name='Preview Product'),

    # view Cart Items
    url(r'^cart_buy/$','mericart.views.cart_buy_view',name='Cart Buy'),

    # view Cart Items
    url(r'^shipping/$','mericart.views.shipping_view',name='Shipping'),
    url(r'^pay/$','mericart.views.pay_view',name='Payment'),
    url(r'^delete_item/(?P<cid>\d+)$','mericart.views.delete_view',name='Delete Cart'),

    #searching
    url(r'^search/$','mericart.views.search_view',name='Search Cart'),
    url(r'^search/(?P<cid>\d+)$','mericart.views.search_b_view',name='Search Brand'),
    url(r'^search_c/(?P<cid>\d+)$','mericart.views.search_c_view',name='Search Cat'),

    #thank you
    url(r'^thank_you/(?P<cid>\w+)$','mericart.views.thank_you_view',name='Thank You'),
    url(r'^orders/$','mericart.views.my_order_view',name='My Order'),
    
) + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
