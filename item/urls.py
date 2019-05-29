from django.conf.urls import url

from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = "item"

urlpatterns = [
    url(r'^items/$', views.SortFormView.as_view(), name='items'),
    url(r'^regist/$', views.regist, name='regist'),
]
