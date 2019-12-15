from django.urls import path

from . import views


urlpatterns = [
    path('', views.initiateGameView),
    path('start/', views.displayGameView),
    path('submit/', views.submitGameView),
    path('waitforscore/',views.waitForScoreView)
]
