from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView,TokenVerifyView
from .views import ConsumerView, CurrentUserView,UserListView,TeamLeadViewSet

router = DefaultRouter()
router.register('teamlead',TeamLeadViewSet)

urlpatterns = [
    path('consumer/',ConsumerView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('users/', UserListView.as_view()),
    path('me/', CurrentUserView.as_view()),
    path('',include(router.urls))
]