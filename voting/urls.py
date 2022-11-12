from django.urls import path

from . import views
app_name = 'voting'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:item_id>/', views.vote_multiple_choice,
         name='vote_multiple_choice'),
    path('<int:item_id>/', views.vote_yna, name='vote_yna'),
]
