from django.urls import path

from robots.views import robot_api, download_excel

urlpatterns = [
    path('robot/', robot_api, name='robot_api'),
    path('download_excell/', download_excel, name='download_excell')
]
