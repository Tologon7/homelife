from rest_framework import serializers
from django.db.models import Avg
from .models import Product, Category, Color, Brand, Review, Banner
from .utils import round_to_nearest_half

class CategorySerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['label', 'value']

    def get_value(self, obj):
        translation = {
            'холодильник': 'refrigerator',
            'стиральная машина': 'washing machine',
            'посудомоечная машина': 'dishwasher',
            'микроволновая печь': 'microwave',
            'телевизор': 'television',
            'пылесос': 'vacuum cleaner',
            'кондиционер': 'air conditioner',
            'печь': 'oven',
            'фен': 'hair dryer',
            'тостер': 'toaster',
            'кофеварка': 'coffee maker',
            'электрический чайник': 'electric kettle',
            'утюг': 'iron',
            'блендер': 'blender',
            'соковыжималка': 'juicer',
            'сушилка для белья': 'clothes dryer',
            'кухонный комбайн': 'food processor',
            'вентилятор': 'fan',
            'холодильная камера': 'cold storage',
            'водонагреватель': 'water heater',
            'мясорубка': 'meat grinder',
            'вафельница': 'waffle maker',
            'суповарка': 'soup maker',
            'электрическая духовка': 'electric oven',
            'мясопереработчик': 'meat slicer',
            'бассейн': 'pool',
            'система фильтрации воды': 'water filtration system',
            'кухонные весы': 'kitchen scale',
            'размораживатель': 'defroster',
            'хлебопечка': 'bread maker',
        }

        # Если значение value уже есть
        if obj.value:
            return translation.get(obj.value, obj.value)

        # Если value нет, присваиваем его на основе label
        return translation.get(obj.label.lower(), obj.label.lower())

    def create(self, validated_data):
        label = validated_data.get('label')

        translation = {
            'холодильник': 'refrigerator',
            'стиральная машина': 'washing machine',
            'посудомоечная машина': 'dishwasher',
            'микроволновая печь': 'microwave',
            'телевизор': 'television',
            'пылесос': 'vacuum cleaner',
            'кондиционер': 'air conditioner',
            'печь': 'oven',
            'фен': 'hair dryer',
            'тостер': 'toaster',
            'кофеварка': 'coffee maker',
            'электрический чайник': 'electric kettle',
            'утюг': 'iron',
            'блендер': 'blender',
            'соковыжималка': 'juicer',
            'сушилка для белья': 'clothes dryer',
            'кухонный комбайн': 'food processor',
            'вентилятор': 'fan',
            'холодильная камера': 'cold storage',
            'водонагреватель': 'water heater',
            'мясорубка': 'meat grinder',
            'вафельница': 'waffle maker',
            'суповарка': 'soup maker',
            'электрическая духовка': 'electric oven',
            'мясопереработчик': 'meat slicer',
            'бассейн': 'pool',
            'система фильтрации воды': 'water filtration system',
            'кухонные весы': 'kitchen scale',
            'размораживатель': 'defroster',
            'хлебопечка': 'bread maker',
        }

        # Присваиваем value на основе label
        validated_data['value'] = translation.get(label.lower(), label.lower())

        return super().create(validated_data)

class ColorSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    class Meta:
        model = Color
        fields = ['label', 'value']

    def get_value(self, obj):
        # Словарь для перевода значений на английский
        translation = {
            'белый': 'white',
            'черный': 'black',
            'красный': 'red',
            'синий': 'blue',
            'зеленый': 'green',
            'желтый': 'yellow',
            'оранжевый': 'orange',
            'пурпурный': 'purple',
            'розовый': 'pink',
            'серый': 'gray',
            'коричневый': 'brown',
            'бежевая': 'beige',
            'фиолетовый': 'violet',
            'голубой': 'light blue',
            'бирюзовый': 'turquoise',
            'мятный': 'mint',
            'лавандовый': 'lavender',
            'гранатовый': 'pomegranate',
            'песочный': 'sand',
            'оливковый': 'olive',
            'малахитовый': 'malachite',
            'медный': 'copper',
            'слоновая кость': 'ivory',
        }

        # Проверяем, есть ли значение
        if obj.value:
            # Возвращаем значение на английском, если оно есть в словаре
            return translation.get(obj.value, obj.value)

        # Если значения нет, возвращаем значение на английском по label
        return translation.get(obj.label.lower(), obj.label.lower())

    def create(self, validated_data):
        label = validated_data.get('label').lower()

        # Словарь для перевода значений на английский
        translation = {
            'белый': 'white',
            'черный': 'black',
            'красный': 'red',
            'синий': 'blue',
            'зеленый': 'green',
            'желтый': 'yellow',
            'оранжевый': 'orange',
            'пурпурный': 'purple',
            'розовый': 'pink',
            'серый': 'gray',
            'коричневый': 'brown',
            'бежевая': 'beige',
            'фиолетовый': 'violet',
            'голубой': 'light blue',
            'бирюзовый': 'turquoise',
            'мятный': 'mint',
            'лавандовый': 'lavender',
            'гранатовый': 'pomegranate',
            'песочный': 'sand',
            'оливковый': 'olive',
            'малахитовый': 'malachite',
            'медный': 'copper',
            'слоновая кость': 'ivory',
        }

        # Присваиваем value на основе label
        validated_data['value'] = translation.get(label, label)

        return super().create(validated_data)
class BrandSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = ['label', 'value']

    def get_value(self, obj):
        translation = {
            'Acer': 'ACER',
            'Amazon': 'AMAZON',
            'Apple': 'APPLE',
            'Asus': 'ASUS',
            'Barnes & Noble': 'BARNES & NOBLE',
            'Blackberry': 'BLACKBERRY',
            'Bosch': 'BOSCH',
            'Bose': 'BOSE',
            'Canon': 'CANON',
            'Dell': 'DELL',
            'Denon': 'DENON',
            'Garmin': 'GARMIN',
            'Hewlett Packard': 'HEWLETT PACKARD',
            'Htc': 'HTC',
            'Lenovo': 'LENOVO',
            'LG': 'LG',
            'Microsoft': 'MICROSOFT',
            'Motorola': 'MOTOROLA',
            'Newegg': 'NEWEGG',
            'Nexus': 'NEXUS',
            'Nikon': 'NIKON',
            'Nokia': 'NOKIA',
            'Olloclip': 'OLLOCLIP',
            'Olympus': 'OLYMPUS',
            'Panasonic': 'PANASONIC',
            'Philips': 'PHILIPS',
            'Pioneer': 'PIONEER',
            'Radioshack': 'RADIOSHACK',
            'Ricoh': 'RICOH',
            'Samsung': 'SAMSUNG',
            'Sharp': 'SHARP',
            'Sony': 'SONY',
            'Tomtom': 'TOMTOM',
            'Toshiba': 'TOSHIBA',
            'Xbox': 'XBOX',
        }

        # Если значение value уже есть
        if obj.value:
            return translation.get(obj.value, obj.value).upper()

        # Если value нет, присваиваем его на основе label
        return translation.get(obj.label, obj.label).upper()

    def create(self, validated_data):
        label = validated_data.get('label')

        translation = {
            'Acer': 'ACER',
            'Amazon': 'AMAZON',
            'Apple': 'APPLE',
            'Asus': 'ASUS',
            'Barnes & Noble': 'BARNES & NOBLE',
            'Blackberry': 'BLACKBERRY',
            'Bosch': 'BOSCH',
            'Bose': 'BOSE',
            'Canon': 'CANON',
            'Dell': 'DELL',
            'Denon': 'DENON',
            'Garmin': 'GARMIN',
            'Hewlett Packard': 'HEWLETT PACKARD',
            'Htc': 'HTC',
            'Lenovo': 'LENOVO',
            'LG': 'LG',
            'Microsoft': 'MICROSOFT',
            'Motorola': 'MOTOROLA',
            'Newegg': 'NEWEGG',
            'Nexus': 'NEXUS',
            'Nikon': 'NIKON',
            'Nokia': 'NOKIA',
            'Olloclip': 'OLLOCLIP',
            'Olympus': 'OLYMPUS',
            'Panasonic': 'PANASONIC',
            'Philips': 'PHILIPS',
            'Pioneer': 'PIONEER',
            'Radioshack': 'RADIOSHACK',
            'Ricoh': 'RICOH',
            'Samsung': 'SAMSUNG',
            'Sharp': 'SHARP',
            'Sony': 'SONY',
            'Tomtom': 'TOMTOM',
            'Toshiba': 'TOSHIBA',
            'Xbox': 'XBOX',
        }

        # Присваиваем value на основе label
        validated_data['value'] = translation.get(label, label).upper()

        return super().create(validated_data)

class ReviewSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'rating', 'comments']



class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    color = ColorSerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    reviews = ReviewSummarySerializer(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()



    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'category',
            'color',
            'images',
            'price',
            'promotion',
            'brand',
            'quantity',
            'description',
            'is_product_of_the_day',
            'reviews',
            'avg_rating',
            'is_active',

        ]

    def get_avg_rating(self, obj):
        if obj.reviews.exists():
            avg_rating = obj.reviews.aggregate(Avg('rating'))['rating__avg']
            return round_to_nearest_half(avg_rating)
        return 0

    def get_images(self, obj):
        request = self.context.get('request')
        images = [
            obj.image1.url if obj.image1 else None,
            obj.image2.url if obj.image2 else None,
            obj.image3.url if obj.image3 else None,
        ]
        return [request.build_absolute_uri(image) for image in images if image] if request else images


class ProductShortSerializer(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'images',
            'avg_rating',
            'title',
            'price',
            'promotion',
        ]

    def get_avg_rating(self, obj):
        if obj.reviews.exists():
            avg_rating = obj.reviews.aggregate(Avg('rating'))['rating__avg']
            return round_to_nearest_half(avg_rating)
        return 0

    def get_images(self, obj):
        request = self.context.get('request')
        images = [
            obj.image1.url if obj.image1 else None,
            obj.image2.url if obj.image2 else None,
            obj.image3.url if obj.image3 else None,
        ]
        if request:
            return [request.build_absolute_uri(image) for image in images if image]
        return [image for image in images if image]





class ProductCreateSerializer(serializers.ModelSerializer):


    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'category',
            'color',
            'image1',
            'image2',
            'image3',
            'price',
            'promotion',
            'brand',
            'quantity',
            'description',
            'is_product_of_the_day',

        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            images = [
                request.build_absolute_uri(instance.image1.url) if instance.image1 else None,
                request.build_absolute_uri(instance.image2.url) if instance.image2 else None,
                request.build_absolute_uri(instance.image3.url) if instance.image3 else None,
            ]
            representation['images'] = [image for image in images if image]
        if not instance.reviews.exists():
            representation.pop('reviews', None)
        return representation

    def create(self, validated_data):
        characteristics_data = validated_data.pop('characteristics', [])
        product = Product.objects.create(**validated_data)
        for characteristic_data in characteristics_data:
            characteristic, created = Characteristic.objects.get_or_create(**characteristic_data)
            product.characteristics.add(characteristic)
        return product

class ReviewSerializer(serializers.ModelSerializer):

    product_title = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id',
            'product',
            'product_title',
            'user',
            'user_name',
            'comments',
            'rating',
            'created',
            'updated'
        ]

    def get_product_title(self, obj):
        return obj.product.title if obj.product else 'unknown'

    def get_user_name(self, obj):
        return obj.user.first_name if obj.user else 'unknown'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('product', None)
        representation.pop('user', None)
        return representation


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'
