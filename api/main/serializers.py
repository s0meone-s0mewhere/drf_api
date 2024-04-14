"""
https://www.django-rest-framework.org/api-guide/relations/
https://www.django-rest-framework.org/api-guide/serializers/
https://www.django-rest-framework.org/api-guide/fields/
https://www.django-rest-framework.org/api-guide/relations/
https://habr.com/ru/companies/yandex_praktikum/articles/598349/
how to send filesin nested json in postman https://stackoverflow.com/questions/30351869/sending-nested-json-object-with-file-using-postman
"""
from rest_framework import serializers
from .models import User, Publication, Feedback, Photo
import datetime as dt
from slugify import slugify #https://pypi.org/project/python-slugify/
from django.contrib.auth.hashers import make_password
import re


def username_validator(value):
    reg = r'^[\w]+$'
    if not bool(re.match(reg, value, flags=re.ASCII)):
        raise serializers.ValidationError('username contains incorrect symbols')

class PhotoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Photo
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class PublicationSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, source='photo_set') 

    def create(self, validated_data):
        if 'rating' in validated_data:
            del validated_data['rating']

        slug = slugify(validated_data['name'], separator='_')
        photos_data = validated_data.pop('photo_set')
        currrent_date = str(dt.datetime.now().strftime('%Y-%m-%d'))
        author = self.context['request'].user
        publication = Publication.objects.create(author=author, slug=slug, publication_date=currrent_date, **validated_data)
        for photo_data in photos_data:
            Photo.objects.create(publication=publication, author=author, **photo_data)
        return publication    
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.slug = slugify(validated_data.get('name', instance.name), separator='_')
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.save()

        if 'photo_set' in validated_data:
            photos_data = validated_data.pop('photo_set')
            for photo_data in photos_data:
                photo_id = photo_data.get('id', None)
                if photo_id:
                    photo = Photo.objects.get(id=photo_id, author=self.context['request'].user, publication=instance)
                    photo.photo = photo_data.get('photo', photo.photo)
                    photo.save()
                else:
                    Photo.objects.create(id=photo_id, author=self.context['request'].user, publication=instance, **photo_data)

        return instance
    

    class Meta:
        model = Publication
        fields = ['id', 'author', 'name', 'slug', 'description', 'price', 'publication_date', 'photos']
        extra_kwargs = {
            'author': {'read_only': True}, 
            'publication_date': {'read_only': True}, 
            'slug': {'read_only': True}, 
        }

        


class UserSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(read_only=True)
    publications = PublicationSerializer(many=True, read_only=True)
    feedbacks = FeedbackSerializer(many=True, read_only=True,)
    
    def update(self, instance, validated_data):
        instance.password = validated_data.get('password', instance.password)
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.user_photo = validated_data.get('user_photo', instance.user_photo)
        instance.save()
        return instance


    class Meta:
        model = User
        exclude = ['last_login', 'is_superuser', 'is_staff', 'groups', 'user_permissions']
        read_only_fields = ['id', 'is_seller', 'date_joined', 'rating', 'is_active', 'verified']
        extra_kwargs = {'username': {'validators': [username_validator]}}
