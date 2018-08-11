from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('icos/', views.ICOListView.as_view(), name='icos'),
    path('icos/<int:pk>', views.ICODetailView.as_view(), name='ico-detail'),
]
