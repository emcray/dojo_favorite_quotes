from django.urls import path
from . import views

urlpatterns=[
    path('', views.home, name='home'),
    path('profile', views.profile),
    path('create_quote', views.create_quote),
    path('update_user/<int:user_id>', views.update_user),
    path('posted_by/<int:user_id>', views.user_quotes),
    path('like/<int:quote_id>', views.like),
    path('delete/<int:quote_id>', views.delete),
    path('logout', views.logout, name = 'logout'),
]