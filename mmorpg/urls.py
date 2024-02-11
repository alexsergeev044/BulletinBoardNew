from django.urls import path

from .views import (AdsList, AdsDetail, AdsCreate, AdsEdit, AdsDelete,
                    MyResponseList, AdsResponseList, ResponseCreate, ResponseDetail,
                    ResponseEdit, ResponseAccept, ResponseDelete)

urlpatterns = [
   path('', AdsList.as_view(), name='ads_list'),
   path('<int:pk>/', AdsDetail.as_view(), name='ads_detail'),
   path('create/', AdsCreate.as_view(), name='ads_create'),
   path('<int:pk>/edit/', AdsEdit.as_view(), name='ads_edit'),
   path('<int:pk>/delete/', AdsDelete.as_view(), name='ads_delete'),
   path('myresponse/', MyResponseList.as_view(), name='myresponse_list'),
   path('adsresponse/', AdsResponseList.as_view(), name='adsresponse_list'),
   path('<int:pk>/response/', ResponseCreate.as_view(), name='response_create'),
   path('<int:apk>/response/<int:pk>/', ResponseDetail.as_view(), name='response_detail'),
   path('<int:apk>/response/<int:pk>/edit/', ResponseEdit.as_view(), name='response_edit'),
   path('<int:apk>/response/<int:pk>/accept/', ResponseAccept.as_view(), name='response_accept'),
   path('<int:apk>/response/<int:pk>/delete/', ResponseDelete.as_view(), name='response_delete'),
]
