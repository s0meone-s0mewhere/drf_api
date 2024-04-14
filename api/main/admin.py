#https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#inlinemodeladmin-objects
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


class PhotoInline(admin.StackedInline):
    verbose_name = 'Фото'
    verbose_name_plural = 'Фото'
    model = models.Photo



class PublicationAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'price', 'publication_date', 'is_active',)
    list_display_links = ('name',)
    inlines = [PhotoInline,]


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_photo', 'is_seller' , 'verified', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined',)
    list_display_links = ('username',)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('author', 'to', 'mark')
    list_display_links = ('author', 'to')


admin.site.register(models.Feedback, FeedbackAdmin)    
admin.site.register(models.Publication, PublicationAdmin)
admin.site.register(models.User, UserAdmin)