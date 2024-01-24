
from django.urls import path
# from . import views
from .views import inf_home, create, MyUpdate, MyDelete, MyAddTovar, MyDeleteTovar, \
    MyAddIm, MyDelIm, myDinamic

urlpatterns = [
    path('', inf_home, {'MytypeData': ''}, name='inf_home'),
    path('horse', inf_home, {'MytypeData': 'horse'}, name='inf_home_h'),
    path('rider', inf_home, {'MytypeData': 'rider'}, name='inf_home_r'),
    path('stable', inf_home, {'MytypeData': 'stable'}, name='inf_home_s'),
    path('create', create, name='inf_cr'),
    path('<int:pk>', myDinamic, name='dinamic'),
    path('<int:pk>/update', MyUpdate.as_view(), name='dinamic-up'),
    path('<int:pk>/delete', MyDelete.as_view(), name='dinamic-del'),
    path('<int:pk>/add_pic', MyAddIm, name='add_picture'),
    path('<int:pk>/del_pic', MyDelIm, name='del_pic'),
    path('<int:pk>/add_tovar', MyAddTovar, name='add_tovar'),
    path('<int:pk>/del_tovar', MyDeleteTovar, name='del_tovar'),
]