import json
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
import uuid 
from django.shortcuts import render, get_object_or_404, redirect
from .models import User
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return HttpResponse("Hello, world. You're at the hello index.")


       

def parse_json(request):
    try:
        return json.loads(request.body.decode('utf-8'))
    except Exception as e:
        return None

# CREATE
@csrf_exempt
def user_create(request):
    if request.method == 'POST':
        data = parse_json(request)
        if not data:
            return HttpResponseBadRequest('Ошибка парсинга JSON')
        if User.objects.filter(card_id=data.get('card_id')).exists() or User.objects.filter(td_username=data.get('td_username')).exists():
            return HttpResponseBadRequest('Пользователь с таким card_id или td_username уже существует')
        user = User.objects.create(
            id= uuid.uuid4(),
            role=data.get('role'),
            card_id=data.get('card_id'),
            td_username=data.get('td_username'),
            excursions=data.get('excursions', '')
        )
        return JsonResponse({'id': user.id, 'role': user.role, 'card_id': user.card_id, 'td_username': user.td_username, 'excursions': user.excursions})
    return HttpResponseBadRequest('Только POST запрос')

# READ (list)
@csrf_exempt
def user_list(request):
    users = User.objects.all().values()
    return JsonResponse(list(users), safe=False)

# READ (detail)
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return JsonResponse({
        'id': user.id,
        'role': user.role,
        'card_id': user.card_id,
        'td_username': user.td_username,
        'excursions': user.excursions
    })

# UPDATE
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        data = parse_json(request)
        if not data:
            return HttpResponseBadRequest('Ошибка парсинга JSON')
        user.role = data.get('role', user.role)
        user.card_id = data.get('card_id', user.card_id)
        user.td_username = data.get('td_username', user.td_username)
        user.excursions = data.get('excursions', user.excursions)
        user.save()
        return JsonResponse({'id': user.id, 'role': user.role, 'card_id': user.card_id, 'td_username': user.td_username, 'excursions': user.excursions})
    return HttpResponseBadRequest('Только POST запрос')

# DELETE
@csrf_exempt
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return JsonResponse({'result': 'deleted'})
    return HttpResponseBadRequest('Только POST запрос')    
