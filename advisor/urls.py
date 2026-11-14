from django.urls import path
from .views import BodyAnalysisView, SkinAnalysisView

urlpatterns = [
    path("skin/", SkinAnalysisView.as_view()),
    path("body/", BodyAnalysisView.as_view()),
]