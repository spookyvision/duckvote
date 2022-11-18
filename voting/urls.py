from django.urls import path
from . import views
from django.views.generic import TemplateView
app_name = 'voting'


urlpatterns = [
    path('', views.index, name='index'),
    path('stats', views.stats, name='stats'),
    path('go/<user_id>',
         views.do_login, name='login'),
    path('logout',
         views.do_logout, name='logout'),
    path('logged_out', TemplateView.as_view(
        template_name='voting/logged_out.html'), name='logged_out'),
    path('yna/<int:yna_id>/create',
         views.YNACreateView.as_view(), name='create_yna'),
    path('yna/<int:yna_id>/update/<int:pk>',
         views.YNAUpdateView.as_view(), name='update_yna'),
]
