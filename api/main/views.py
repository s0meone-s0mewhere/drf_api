"""
https://www.django-rest-framework.org/api-guide/viewsets/
https://stackoverflow.com/questions/31920853/aggregate-and-other-annotated-fields-in-django-rest-framework-serializers
"""
from typing import Any
from rest_framework import viewsets
from .serializers import UserSerializer, PublicationSerializer, FeedbackSerializer, PhotoSerializer
from .models import User, Publication, Feedback, Photo 
from .permissions import IsOwnerOrReadOnly
from django.db.models import Avg
from rest_framework.views import APIView
from .utils import signer
from django.core.signing import BadSignature
from rest_framework.response import Response
from rest_framework.exceptions import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from .utils import send_activation_notification



class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsOwnerOrReadOnly,]


class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    permission_classes = [IsOwnerOrReadOnly,]
    lookup_field = 'slug'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly,]
    lookup_field = 'username'

    def get_queryset(self):
        queryset = User.objects.annotate(rating=Avg('feedbacks__mark'))
        return queryset


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsOwnerOrReadOnly]


class UserActivation(APIView):
    def get(self, request, sign):
        try:
            username = signer.unsign(sign)
        except BadSignature:
            return Response("Bad signature", status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, username=username)
        if user.verified:
            return Response('user already activated', status=status.HTTP_200_OK)
        else:
            user.verified = True
            user.save()
            return Response('Email is successfully activated')
        

class UserActivationResend(APIView):
    def get(self, request):
        if request.user:
            send_activation_notification(request.user)
            return Response('Verification email sent', status=status.HTTP_200_OK)
        

        
        