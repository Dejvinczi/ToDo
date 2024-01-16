"""Todo url's"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api import views

router = DefaultRouter()
router.register('tasks', views.TaskViewSet, basename='task')
router.register('tags', views.TagViewSet, basename='tag')


urlpatterns = [
    path('', include(router.urls))
]
