from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeveloperViewSet, GameViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'developers', DeveloperViewSet, basename='developer')
router.register(r'games', GameViewSet, basename='game')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]