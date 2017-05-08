from django.conf.urls import url
from .views import StepsView

urlpatterns = [
    url(r'steps/(?P<step_type>[a-z]+)/$', StepsView.as_view())
]
