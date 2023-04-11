from venv import create
from django.conf.urls import url
from django.urls import path
from boxes import views


urlpatterns = [
    path('create/',views.CreateBoxView.as_view(),name='create-box'),
    path('create_config/',views.CreateConflig.as_view(),name='create-conflig'),
    path('list/', views.BoxListView.as_view(), name="list_view"),
    path('list/my_boxes/', views.MyBoxListView.as_view(), name="my_list_view"),
    path('delete/<int:pk>', views.BoxDeleteView.as_view(), name="delete_view"),
    path('update/<int:pk>',views.BoxUpdates.as_view(),name="update"),
    path('update_config/',views.UpdadeConfig.as_view(),name="update"),
    path('api/login',views.login),
    path('update_config/',views.BoxUpdateConfigs.as_view(),name="update_config"),
    path('get_config/',views.BoxConfigs.as_view(),name="get_config"),
]
