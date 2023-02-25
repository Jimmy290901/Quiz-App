from re import search
from django.contrib.messages import api
from django.contrib.messages.api import success
from rest_framework.fields import DateField
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import UserSerializer

# Create your views here.

# def listUsers(request):
#     if request.method == 'GET':
#         users = User.objects.all()
#         serializer = UserSerializer(users, many = True)
#         return JsonResponse(serializer.data, safe=False)
# @api_view(['POST'])
# def login(request):
#     if request.method == 'POST':
#         print(request.data['username'])
#         user = authenticate(username = request.data['username'], password = request.data['password'])
#         if user is not None:
#             successMessage = {'message':'User Login Successfully'}
#             return Response(successMessage, status=status.HTTP_202_ACCEPTED)
#         message = {'message':'Username/Password Incorrect'}
#         return Response(message, status = status.HTTP_406_NOT_ACCEPTABLE)

# @csrf_exempt
# def signup(request):
#     if request.method == 'POST':
#         # details = request.POST
#         # print(request)
#         # details['password'] = pbkdf2_sha256.encrypt(details['password'], rounds = 12000, salt_size=32)
#         data = JSONParser().parse(request)
#         data['password'] = pbkdf2_sha256.encrypt(data['password'], rounds = 12000, salt_size=32)
#         # print(data)
#         serializer = UserSerializer(data = data)
#         # print(serializer)
#         check_user = User.objects.filter(email = data['email'])
#         if serializer.is_valid() and not check_user.exists():
#             serializer.save()
#             return JsonResponse(serializer.data, status = 201)
#         return JsonResponse(serializer.errors, status = 400)
#         # return HttpResponse('Hello')

# @api_view(['POST'])
# def signup(request):
#     if request.method == 'POST':
#         serializer = UserSerializer(data = request.data)
#         print(serializer.data)
#         if serializer.is_valid():
#             User.objects.create_user(serializer.data)
#             successMessage = {'message':'User Created Successfully'}
#             return Response(successMessage, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        