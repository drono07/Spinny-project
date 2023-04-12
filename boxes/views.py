from http.client import HTTPResponse
import imp
from urllib import response
from xmlrpc.client import ResponseError
from .models import Boxes , Config
from rest_framework.views import APIView
from boxes.utils import BoxUtils
from boxes.serializer import StaffBoxesSerializer,BoxesSerializer
from .filters import BoxFilter, MyBoxFilter
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
import bdb, json
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
        if is_valid_user & check_validity(user):
            length = int(request.data.get('length'))
            breadth = int(request.data.get('breadth'))
            height = int(request.data.get('height'))
            box,status = BoxUtils.create_box(length=length, breadth=breadth, height=height, user=user)
            return Response(StaffBoxesSerializer(box).data , status= status)
        if is_valid_user:
            return Response("Box Limit Exceed")
        return Response("User is Not Staff Member ",status=401)

class CreateConflig(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request, *args ,**kwargs):
        user = request.user
        is_valid_user = BoxUpsertValidations.validate_create_box(user)
        if is_valid_user:
            average_area = int(request.data.get('average_area'))
            average_volume = int(request.data.get('average_volume'))
            tolal_boxes  = int(request.data.get('total_boxes'))
            total_boxes_user = int(request.data.get('total_boxes_user'))
            config = BoxUtils.create_config(average_area = average_area , average_volume= average_volume ,\
                total_boxes=tolal_boxes, total_boxes_user= total_boxes_user )
            return Response("Boxes Config Created", status= 200)
        else:
            return Response("User is Not Staff Member" , status=401)
        
class BoxListView(generics.ListAPIView):
    queryset = Boxes.objects.all()
    serializer_class = StaffBoxesSerializer
    permission_classes = [IsAuthenticated,]
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = BoxFilter

    def get_serializer_class(self):
        if not self.request.user.is_staff :
            return BoxesSerializer 
        return super().get_serializer_class()

class MyBoxListView(generics.ListAPIView):
    serializer_class = StaffBoxesSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = MyBoxFilter

    def get_queryset(self):
        is_staff_user = BoxUpsertValidations.validate_my_box_list_request(self.request.user)
        
        if not is_staff_user:
            return Boxes.objects.none()
        return Boxes.objects.filter(created_by=self.request.user.username)
    
class BoxDeleteView(APIView):
    permission_classes = [IsAuthenticated,]
    def delete(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            box=Boxes.objects.get(id=id)
        except  Boxes.DoesNotExist:
            return Response("No Box Exists With This Id {}".format(id))
    
        is_user_valid=BoxUpsertValidations.validate_delete_box(user=request.user,box=box)
        if is_user_valid:
            box.delete()
            return Response("Box Deleted")
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
        try:
            box=Boxes.objects.get(id=id)
        except Boxes.DoesNotExist:
            return Response("Invalid Id",status=400)
        if is_valid_user:
            if length:
                box.length =length
            if breadth:
                box.breadth=breadth
            if height:
                box.height =height
                # area,vol = BoxUtils.calculate_area_volume(length=box.length, breadth=box.breadth, height=box.height)
                # box.area=area
                # box.volume=vol
                box.save()
                return Response("Succesfully Updated",status=200)
        return response("User is not staff member", status = 401)

class UpdadeConfig(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self,request,*args , **kwargs):
        id = kwargs.get("pk")
        user= request.user
        is_valid_user=BoxUpsertValidations.validate_update_box_request(user)
        average_area = request.data.get('average_area')
        average_volume= request.data.get('average_volume')
        total_boxes= request.data.get('total_boxes')
        total_boxes_user = request.data.get('total_boxes_user')
        try:
            config=Config.objects.get(id=id)
        except Config.DoesNotExist:
            return Response("User Id is not Valid")
        if is_valid_user:
            if average_area:
                config.average_area =average_area
            if average_volume:
                config.average_volume=average_volume
            if total_boxes:
                config.total_boxes =total_boxes
            if total_boxes_user:
                config.total_boxes_user = total_boxes_user
            Config.objects.filter(active=True).update(active = False)
            config.active = True
            config.save()
            return Response("Succesfully Updated",status=200)
        return response("User is not staff member", status = 401)


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


    
