from django.urls import path
from . import views
app_name = 'voting'
urlpatterns = [
    path('', views.index, name='index'),
    path('mc/<int:item_id>/', views.vote_multiple_choice,
         name='vote_multiple_choice'),
    path('yna/<int:item_id>/', views.vote_yna, name='edit_yna'),
    path('yna/<int:yna_id>/create',
         views.YNACreateView.as_view(), name='create_yna'),
    path('yna/update/<int:pk>',
         views.YNAUpdateView.as_view(), name='update_yna'),
]
