from django.conf.urls import url, include
from django.contrib import admin
from tastypie.api import Api

from netAngels.v1_api.api import CodeLinkResource
from netAngels.views import home, all_links, new_link, get_from_hash, redirect_from_short

# api (tastypie) universal function for conversion
v1_api = Api(api_name='v1')
v1_api.register(CodeLinkResource())

urlpatterns = [
    url(r'^admin/', admin.site.urls),  # admin panel

    url(r'^all/', all_links),  # browse all links, deleting links, detailed view
    url(r'^new_link/?(\d*)/', new_link),  # detailed link view
    url(r'^hash/redirect/?(\d*)/', redirect_from_short),  # get full url from hash
    url(r'^hash/', get_from_hash),  # get full url from hash
    url(r'^$', home),  # make short url (hash) from full url and view 20 most popular links

    url(r'^api/', include(v1_api.urls)),  # api (tastypie) support (see v1_api/api.py)

]
