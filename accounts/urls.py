from django.urls import path
from . import views, serializers

urlpatterns = [
    path('login/', serializers.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),

    path('register/', views.register, name='register'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),

    path('reset-password/<uidb64>/<token>/',
         views.reset_password, name='reset_password'),

    path('reset-password/', views.reset_password_data, name='reset_password_data'),

]
