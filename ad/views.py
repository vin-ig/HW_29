from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic import UpdateView

from ad.models import Ad
from ad.serializers import AdSerializer, AdCreateSerializer, AdUpdateSerializer
from user.serializers import UserDestroySerializer


@method_decorator(csrf_exempt, name='dispatch')
class IndexView(View):
	def get(self, request):
		return JsonResponse({'status': 'ok'}, status=200)


class AdListView(ListAPIView):
	queryset = Ad.objects.all()
	serializer_class = AdSerializer

	def get(self, request, *args, **kwargs):
		cat_filter = request.GET.get('cat')
		if cat_filter:
			self.queryset = self.queryset.filter(category_id__in=cat_filter)
		return super().get(request, *args, **kwargs)


class AdDetailView(RetrieveAPIView):
	queryset = Ad.objects.all()
	serializer_class = AdSerializer


class AdCreateView(CreateAPIView):
	queryset = Ad.objects.all()
	serializer_class = AdCreateSerializer


class AdUpdateView(UpdateAPIView):
	queryset = Ad.objects.all()
	serializer_class = AdUpdateSerializer


class AdDeleteView(DestroyAPIView):
	queryset = Ad.objects.all()
	serializer_class = UserDestroySerializer


@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
	model = Ad
	fields = ['name', 'author', 'price', 'description', 'image', 'is_published', 'category']

	def post(self, request, *args, **kwargs):
		ad = self.get_object()

		ad.image = request.FILES['image']
		ad.save()

		return JsonResponse({
			'id': ad.id,
			'name': ad.name,
			'author': ad.author.username,
			'price': ad.price,
			'description': ad.description,
			'image': ad.image.url if ad.image else None,
			'is_published': ad.is_published,
			'category': ad.category.name,
		}, safe=False)
