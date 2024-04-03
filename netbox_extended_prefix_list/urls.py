from django.urls import path

from . import views

urlpatterns = [
    path('prefixes/', views.ExtendedPrefixListView.as_view(), name='prefix_list'),
]
