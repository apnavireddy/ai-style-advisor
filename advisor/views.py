from django.shortcuts import render

# Create your views here.
import os
import tempfile

from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .engine.pipeline import analyse_body, analyse_skin
from .serializers import BodyRequestSerializer, SkinRequestSerializer


class SkinAnalysisView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = SkinRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = serializer.validated_data["image"]

        suffix = os.path.splitext(image.name)[1] or ".jpg"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            for chunk in image.chunks():
                tmp.write(chunk)
            path = tmp.name

        try:
            result = analyse_skin(path)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        finally:
            os.remove(path)  # never keep the user's photo

        return Response(result)


class BodyAnalysisView(APIView):
    def post(self, request):
        serializer = BodyRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return Response(analyse_body(data["shoulder"], data["bust"], data["waist"], data["hips"]))