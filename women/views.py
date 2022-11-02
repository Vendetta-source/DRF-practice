from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import WomenSerializer


# все три класса ниже (WomenAPIList, WomenAPIUpdate, WomenAPIDetailView) можно запихнуть в один Set класс
class WomenViewSet(viewsets.ModelViewSet):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer

    # переопределение метода
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if not pk:
            return Women.objects.all()[:3]
        return Women.objects.filter(pk=pk)

    # для вывода категории с декоратором
    @action(methods=['get'], detail=True)
    def category(self, request, pk=None):
        category = Category.objects.get(pk=pk)
        return Response({'category': category.name})

    # для вывода списка категорий с декоратором
    @action(methods=['get'], detail=False)
    def categories(self, request):
        categories = Category.objects.all()
        return Response({'categories': [c.name for c in categories]})


# наследование от класса ListCreateAPIView (возвращает и добавляет записи автоматически (GET, POST))
class WomenAPIList(generics.ListCreateAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer


# наследование от класса UpdateAPIView (обновляет записи (PUT, PATCH))
class WomenAPIUpdate(generics.UpdateAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer


# наследование от класса RetrieveUpdateDestroyAPIView (GET, POST, PUT, PATCH, DELETE))
class WomenAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer


# наследование от базового класса DRF
class WomenAPIView(APIView):
    def get(self, request):
        w = Women.objects.all()
        return Response({'posts': WomenSerializer(w, many=True).data})

    def post(self, request):
        serializer = WomenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'post': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Method PUT not allowed'})

        try:
            instance = Women.objects.get(pk=pk)
        except:
            return Response({'error': 'Object does not exists'})

        serializer = WomenSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'post': serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Method DELETE not allowed'})

        try:
            instance = Women.objects.get(pk=pk)
            instance.delete()
        except:
            return Response({'error': 'Object does not exists'})

        return Response({'status': f'Record with number id = {pk} was delete'})

# class WomenAPIView(generics.ListAPIView):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer
