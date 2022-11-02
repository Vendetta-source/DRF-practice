import io
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Women


# сериализатор с помощью ModelSerializer (связанные с моделью Django)
class WomenSerializer(serializers.ModelSerializer):
    # класс Мета заменяет ручное описание полей сериалайзера
    class Meta:
        model = Women
        fields = '__all__'#('title', 'content', 'category')


# сериалайзер с помощью Serializer (базовый класс сериализаторов)
class WomenSerializer1(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    time_create = serializers.DateTimeField(read_only=True)
    time_update = serializers.DateTimeField(read_only=True)
    is_published = serializers.BooleanField(default=True)
    category_id = serializers.IntegerField()

    # метод для создания записи в БД
    def create(self, validated_data):
        return Women.objects.create(**validated_data)

    # метод для обновления записи в БД
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.time_update = validated_data.get('time_update', instance.time_update)
        instance.is_published = validated_data.get('is_published', instance.is_published)
        instance.category_id = validated_data.get('category_id', instance.category_id)
        instance.save()
        return instance


# сериалайзер с помощью ModelSerializer
# class WomenSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Women
#         fields = ('title', 'category_id')

# абстрактное представление модели
# class WomenModel:
#     def __init__(self, title, content):
#         self.title = title
#         self.content = content

# объяснение принципа кодирования в json с помощью сериалайзера
# def encode():
#     model = WomenModel('Angelina Jolie', 'Content: Angelina Jolie')
#     model_sr = WomenSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
#
#
# объяснение принципа декодирования из json с помощью сериалайзера
# def decode():
#     stream = io.BytesIO(b'{"title":"Angelina Jolie","content":"Content: Angelina Jolie"}')
#     data = JSONParser().parse(stream)
#     serializer = WomenSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)
