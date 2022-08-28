from rest_framework import serializers

from category.models import Category
from ad.models import Ad, Category


class AdSerializer(serializers.ModelSerializer):
	category = serializers.SlugRelatedField(
		read_only=True,
		slug_field='name'
	)

	class Meta:
		model = Ad
		fields = '__all__'


class AdCreateSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(read_only=True)
	category = serializers.SlugRelatedField(
		required=False,
		slug_field='name',
		queryset=Category.objects.all(),
	)

	class Meta:
		model = Ad
		exclude = ['image']

	def is_valid(self, raise_exception=False):
		self._category = self.initial_data.pop('category', None)
		return super().is_valid(raise_exception=raise_exception)

	def create(self, validated_data):
		ad = Ad.objects.create(**validated_data)
		if self._category:
			category_obj = Category.objects.get_or_create(name=self._category)[0]
			ad.category = category_obj
			ad.save()
		return ad


class AdUpdateSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(read_only=True)
	category = serializers.SlugRelatedField(
		required=False,
		slug_field='name',
		queryset=Category.objects.all(),
	)

	class Meta:
		model = Ad
		fields = '__all__'

	def is_valid(self, raise_exception=False):
		self._category = self.initial_data.pop('category', None)
		return super().is_valid(raise_exception=raise_exception)

	def save(self):
		ad = super().save()
		if self._category:
			category_obj = Category.objects.get_or_create(name=self._category)[0]
			ad.category = category_obj
			ad.save()
		return ad


class AdDestroySerializer(serializers.ModelSerializer):
	class Meta:
		model = Ad
		fields = ['id']
