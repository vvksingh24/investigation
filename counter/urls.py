from django.conf.urls import url
from .views import HomePage, results

app_name = 'counter'
urlpatterns = [
	url(r'^$',HomePage.as_view(),name='home'),
	url(r'^results/(?P<query>[\w ]+)$', results, name='results'),
]