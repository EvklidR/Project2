from django.urls import path
from .views import prof_v, logout_user, RegisterUser, register, сhangeUserData, addCard, buyTov, delCrCard, UpCrCard, \
    MyDeleteUs

urlpatterns = [
    path('profile/', prof_v, name='prof'),
    path('logout/', logout_user, name='User_logout'),
    path('register/', register, name='User_register'),
    path('<int:pk>/change/', сhangeUserData, name='change'),
    path('addCard/', addCard, name='addCard'),
    path('<int:pk>/BuyTov/', buyTov, name='buy'),
    path('<int:pk>/del_crcard', delCrCard, name='del_card'),
    path('<int:pk>/up_crcard', UpCrCard.as_view(), name='up_card'),
    path('<int:pk>/del_us', MyDeleteUs, name='del_us')
]