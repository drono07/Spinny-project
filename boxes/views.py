
from http.client import HTTPResponse
import imp
from urllib import response
from xmlrpc.client import ResponseError
from .models import Boxes
from rest_framework.views import APIView
from boxes.utils import BoxUtils
from boxes.serializer import BoxesSerializer,AdminBoxSerializer
from .filters import BoxFilter
from rest_framework import status,generics
import django_filters.rest_framework as filters
from rest_framework.permissions import (IsAuthenticated,
                                        IsAdminUser,
                                        IsAuthenticatedOrReadOnly)
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from constance import config
from boxes.validations import BoxUpsertValidations
from .validation import check_validity
from rest_framework.parsers import JSONParser
import bdb
from django.http import HttpResponse

class HomeView(APIView):
    permission_classes = []
    authentication_classes = []
    def get(self, request, *args, **kwargs):
        return HttpResponse("Here's the Home of the web page.")

class CreateBoxView(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request, *args, **kwargs):
        user= request.user
        is_valid_user=BoxUpsertValidations.validate_create_box(user)
        if is_valid_user & check_validity(request.user):
            length = int(request.data.get('length'))
            breadth = int(request.data.get('breadth'))
            height = int(request.data.get('height'))
            box,status = BoxUtils.create_box(length=length, breadth=breadth, height=height, user=user)
            return Response(BoxesSerializer(box).data)
        if is_valid_user:
            return Response("Box Limit Exceed")
        return Response("User is Not Staff Member ")

        
class BoxListView(generics.ListAPIView):
    serializer_class = BoxesSerializer
    permission_classes = [IsAuthenticated,]
    queryset = Boxes.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = BoxFilter

class MyBoxListView(generics.ListAPIView):
    serializer_class = BoxesSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = BoxFilter

    def queryset(self, request):
        return Boxes.objects.filter(created_by=request.user)

    def get(self, request, *args, **kwargs):
        is_staff_user = BoxUpsertValidations.validate_my_box_list_request(request.user)
        if not is_staff_user:
            return Response("not a staff member")
        queryset = self.queryset(request=request)
        filtered_queryset = self.filter_queryset(queryset)
        data = self.serializer_class(filtered_queryset, many=True).data
        return Response(data)
    

class BoxDeleteView(APIView):
    permission_classes = [IsAuthenticated,]
    def delete(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        box=Boxes.objects.filter(id=id)
        is_user_valid=BoxUpsertValidations.validate_delete_box(user=request.user,box=box)
        if is_user_valid:
            box.delete()
            data = dict()
            data["reason"] = "Box Deleted"
        return Response("Only Box Creater can delete")

class BoxUpdates(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        user= request.user
        is_valid_user=BoxUpsertValidations.validate_update_box_request(user)
        length = request.data.get('length')
        breadth= request.data.get('breadth')
        height= request.data.get('height')
        box=Boxes.objects.get(id=id)
        if is_valid_user:
            if length:
                box.length =length
            if breadth:
                box.breadth=breadth
            if height:
                box.height =height
                area,vol = BoxUtils.calculate_area_volume(length=box.length, breadth=box.breadth, height=box.height)
                box.area=area
                box.volume=vol
                box.save()
                return Response("Succesfully Updated")
        return response("User is not staff member")

class BoxUpdateConfigs(APIView):

    def post(self, request, *args, **kwargs):
        max_average_area = request.data.get('max_average_area')
        max_average_volume = request.data.get('max_average_volume')
        max_box_in_week = request.data.get('max_box_in_week')
        max_box_in_week_user = request.data.get('max_box_in_week_user')
        if max_average_area:
            config.MAX_AVERAGE_AREA = max_average_area
        if max_average_volume:
            config.MAX_AVERAGE_VOLUME = max_average_volume
        if max_box_in_week:
            config.MAX_BOXES_ADDED_IN_A_WEEK = max_box_in_week
        if max_box_in_week_user:
            config.MAX_BOXES_ADDED_IN_A_WEEK_BY_USER = max_box_in_week_user
        return Response("config successfully updated")

class BoxConfigs(APIView):

    def get(self, request, *args, **kwargs):
        _config = {
            "max_average_area": config.MAX_AVERAGE_AREA,
            "max_average_volume": config.MAX_AVERAGE_VOLUME,
            "max_box_in_week": config.MAX_BOXES_ADDED_IN_A_WEEK,
            "max_box_in_week_user": config.MAX_BOXES_ADDED_IN_A_WEEK_BY_USER
        }
        return Response(_config)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)
