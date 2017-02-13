import rest_framework
import rest_framework_json_api
from django.contrib.auth import authenticate
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import parsers, exceptions
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import ListAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.views import APIView
from rest_framework_json_api.utils import format_drf_errors

from taskbackend.serializers import AuthSerializer

from taskbackend.models import Project

from taskbackend.serializers import ProjectSerializer


class JsonApiViewSet(viewsets.ModelViewSet):
    """
    This is an example on how to configure DRF-jsonapi from
    within a class. It allows using DRF-jsonapi alongside
    vanilla DRF API views.
    """
    parser_classes = [
        rest_framework_json_api.parsers.JSONParser,
        rest_framework.parsers.FormParser,
        rest_framework.parsers.MultiPartParser,
    ]
    renderer_classes = [
        rest_framework_json_api.renderers.JSONRenderer,
        rest_framework.renderers.BrowsableAPIRenderer,
    ]
    metadata_class = rest_framework_json_api.metadata.JSONAPIMetadata

    def handle_exception(self, exc):
        if isinstance(exc, exceptions.ValidationError):
            # some require that validation errors return 422 status
            # for example ember-data (isInvalid method on adapter)
            exc.status_code = HTTP_422_UNPROCESSABLE_ENTITY
        # exception handler can't be set on class so you have to
        # override the error response in this method
        response = super(JsonApiViewSet, self).handle_exception(exc)
        context = self.get_exception_handler_context()
        return format_drf_errors(response, context, exc)


class AuthView(APIView):
    """
    Authenticating user
    """

    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = AuthSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.data['login']
        password = serializer.data['password']
        print(user + ' ' + password)
        a_user = authenticate(username=user, password=password)
        if a_user is not None:
            token, created = Token.objects.get_or_create(user=a_user)
            return Response({'access_token': token.key})
        return Response({'Message': 'invalid login/password'})


class ProjectsView(JsonApiViewSet):
    """
    Displays projects of current user
    """

    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def get(self, request, **kwargs):
        queryset = self.get_queryset().filter(
            Q(owner=request.user) | Q(projectrole__userprojectrole__user=request.user))
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)
