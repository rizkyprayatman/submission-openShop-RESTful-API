from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from .models import Product
from .serializers import ProductSerializer


class ProductListCreate(APIView):
    def get(self, request):
        name = request.GET.get('name')
        location = request.GET.get('location')
        qs = Product.objects.filter(is_delete=False)
        if name:
            qs = qs.filter(name__icontains=name)
        if location:
            qs = qs.filter(location__icontains=location)
        serializer = ProductSerializer(qs, many=True, context={'request': request})
        return Response({'products': serializer.data})

    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        product = serializer.save()
        data = ProductSerializer(product, context={'request': request}).data
        return Response(data, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):
    def get_object(self, pk, include_deleted=False):
        try:
            if include_deleted:
                return Product.objects.get(pk=pk)
            return Product.objects.get(pk=pk, is_delete=False)
        except Product.DoesNotExist:
            raise NotFound(detail='Not found.')

    def get(self, request, pk):
        product = self.get_object(pk, include_deleted=True)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        product = serializer.save()
        data = ProductSerializer(product, context={'request': request}).data
        return Response(data)

    def delete(self, request, pk):
        product = self.get_object(pk)
        product.is_delete = True
        product.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
