from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (UserRegistrationSerializer,
                          LoginSerializer,
                          ProductSerializer
                          )
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from product.models import Product, Category
from django.http import Http404



class UserRegistrationView(APIView):
    @swagger_auto_schema(request_body=UserRegistrationSerializer)

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(user, status=201)
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # Get the tokens from the serializer
        tokens = serializer.validated_data['tokens']

        return Response(tokens)

class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
class ProductCreateView(APIView):


    permission_classes = [IsAuthenticated]



    @swagger_auto_schema(request_body=ProductSerializer)
    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)




class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)


class ProductUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ProductSerializer)
    def put(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProductDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(status=204)