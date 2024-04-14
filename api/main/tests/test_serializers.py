#https://habr.com/ru/companies/pvs-studio/articles/648717/
#
from django.test import TestCase
from models import User
from serializers import UserSerializer

class UserSerializerTests(TestCase):
    """tests for UserSerializer"""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            
            )
        