"""
https://www.django-rest-framework.org/api-guide/routers/
"""
from django.urls import path
from .views import *
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'publications', PublicationViewSet)
router.register(r'feedbacks', FeedbackViewSet)
urlpatterns = router.urls
urlpatterns += [
    path('verification/resend/', UserActivationResend.as_view(), name='register_resend'),
    path('verification/<str:sign>/', UserActivation.as_view(), name='register_activate'),
    ]