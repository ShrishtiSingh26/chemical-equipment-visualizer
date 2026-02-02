# equipment/urls.py
from django.urls import path
from .views import UploadCSV, History,  GeneratePDF



urlpatterns = [
    path('upload/', UploadCSV.as_view()),
    path('history/', History.as_view()),
    path('report/', GeneratePDF.as_view()),
]
