from django.urls import path
from . import views

urlpatterns = [
    path('create-app/', views.create_app, name='create_app'),
    path('get-all-apps/', views.get_all_apps, name='get_all_apps'),
    path('get-single-app/<int:app_id>/',
         views.get_single_app, name='get_single_app'),
    path('delete-app/<int:app_id>/',
         views.delete_app, name='delete_app'),
    path('update-app/<int:app_id>/',
         views.update_app, name='update_app'),
    path('upgrade-plan/<int:app_id>/',
         views.upgrade_subscription, name='upgrade_subscription'),
]
