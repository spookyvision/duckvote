from django.urls import path
from . import views
app_name = 'voting'
urlpatterns = [
    path('', views.index, name='index'),
    path('stats', views.stats, name='stats'),
    path('go/<user_id>',
         views.do_login, name='login'),

    path('yna/<int:yna_id>/create',
         views.YNACreateView.as_view(), name='create_yna'),
    path('yna/<int:yna_id>/update/<int:pk>',
         views.YNAUpdateView.as_view(), name='update_yna'),
]
