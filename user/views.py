import json

from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic import DetailView, UpdateView, ListView, CreateView, DeleteView

from location.models import Location
from user.models import User


@method_decorator(csrf_exempt, name='dispatch')
class UserListView(ListView):
	model = User

	def get(self, request, *args, **kwargs):
		super().get(request, *args, **kwargs)

		users = self.object_list

		result = []
		for user in users:
			result.append({
				'id': user.id,
				'username': user.username,
				'first_name': user.first_name,
				'last_name': user.last_name,
				'role': user.role,
				'age': user.age,
				'location': user.location.name.split(', ')
			})
		return JsonResponse(result, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserDetailView(DetailView):
	model = User

	def get(self, request, *args, **kwargs):
		super().get(request, *args, **kwargs)
		user = self.get_object()

		return JsonResponse({
			'id': user.id,
			'username': user.username,
			'first_name': user.first_name,
			'last_name': user.last_name,
			'role': user.role,
			'age': user.age,
			'location': user.location.name.split(', ')
		}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
	model = User
	fields = ['username', 'first_name', 'last_name', 'password', 'age', 'role', 'location']

	def post(self, request, *args, **kwargs):
		super().post(request, *args, **kwargs)

		data = json.loads(request.body)
		location_obj = Location.objects.get_or_create(name=', '.join(data.get('location')))[0]

		user = User.objects.create(
			username=data.get('username'),
			first_name=data.get('first_name'),
			last_name=data.get('last_name'),
			password=data.get('password'),
			age=data.get('age'),
			role=data.get('role'),
			location=location_obj,
		)

		return JsonResponse({
			'id': user.id,
			'username': user.username,
			'first_name': user.first_name,
			'last_name': user.last_name,
			'role': user.role,
			'age': user.age,
			'location': user.location.name.split(', ')
		}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
	model = User
	fields = ['username', 'first_name', 'last_name', 'password', 'age', 'role', 'location']

	def patch(self, request, *args, **kwargs):
		super().post(request, *args, **kwargs)

		data = json.loads(request.body)
		user = self.object

		user.username = data.get('username', user.username)
		user.first_name = data.get('first_name', user.first_name)
		user.last_name = data.get('last_name', user.last_name)
		user.password = data.get('password', user.password)
		user.age = data.get('age', user.age)
		user.role = data.get('role', user.role)
		if data.get('location'):
			location_obj = Location.objects.get_or_create(name=', '.join(data.get('location')))[0]
			user.location = location_obj

		user.save()

		return JsonResponse({
			'id': user.id,
			'username': user.username,
			'first_name': user.first_name,
			'last_name': user.last_name,
			'role': user.role,
			'age': user.age,
			'location': user.location.name.split(', ')
		}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
	model = User
	success_url = '/'

	def delete(self, request, *args, **kwargs):
		super().delete(request, *args, **kwargs)

		return JsonResponse({'status': 'ok'})
