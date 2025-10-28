import json
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
import uuid 
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import datetime
import calendar
from hello.models import Visit
from .models import User
from django.db import IntegrityError

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
            id=str(uuid.uuid4()),
            role=data.get('role'),
            card_id=data.get('card_id'),
            td_username=data.get('td_username'),
            excursions=data.get('excursions', ''),
            fullname=data.get('fullname', '')
        )
        return JsonResponse({
            'id': str(user.id),
            'role': user.role,
            'card_id': user.card_id,
            'td_username': user.td_username,
            'excursions': user.excursions,
            'fullname': user.fullname,
            'visit_count': user.visit_count
        })
    return HttpResponseBadRequest('Только POST запрос')

# READ (list)
@csrf_exempt
def user_list(request):
    if request.method != 'GET':
        return HttpResponseBadRequest('Только GET запрос')
    users = User.objects.all()
    result = []
    for u in users:
        result.append({
            'id': str(u.id),
            'role': u.role,
            'card_id': u.card_id,
            'td_username': u.td_username,
            'excursions': u.excursions,
            'fullname': u.fullname,
            'visit_count': u.visit_count
        })
    return JsonResponse(result, safe=False)

# READ (detail)
def user_detail(request, pk):
    if request.method != 'GET':
        return HttpResponseBadRequest('Только GET запрос')

    user = get_object_or_404(User, pk=pk)
    return JsonResponse({
        'id': str(user.id),
        'role': user.role,
        'card_id': user.card_id,
        'td_username': user.td_username,
        'excursions': user.excursions,
        'fullname': user.fullname,
        'visit_count': user.visit_count
    })

# UPDATE
@csrf_exempt
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'UPDATE':
        data = parse_json(request)
        if not data:
            return HttpResponseBadRequest('Ошибка парсинга JSON')

        # проверка уникальности card_id и td_username для других пользователей
        new_card = data.get('card_id', user.card_id)
        if new_card != user.card_id and User.objects.filter(card_id=new_card).exclude(pk=user.pk).exists():
            return HttpResponseBadRequest('card_id уже используется другим пользователем')

        new_td = data.get('td_username', user.td_username)
        if new_td != user.td_username and User.objects.filter(td_username=new_td).exclude(pk=user.pk).exists():
            return HttpResponseBadRequest('td_username уже используется другим пользователем')

        user.role = data.get('role', user.role)
        user.card_id = new_card
        user.td_username = new_td
        user.excursions = data.get('excursions', user.excursions)
        user.fullname = data.get('fullname', user.fullname)
        try:
            user.save()
        except IntegrityError:
            return HttpResponseBadRequest('Нарушение уникальности при сохранении')
        return JsonResponse({
            'id': str(user.id),
            'role': user.role,
            'card_id': user.card_id,
            'td_username': user.td_username,
            'excursions': user.excursions,
            'fullname': user.fullname,
            'visit_count': user.visit_count
        })
    return HttpResponseBadRequest('Только UPDATE запрос')

# DELETE
@csrf_exempt
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'DELETE':
        user.delete()
        return JsonResponse({'result': 'deleted'})
    return HttpResponseBadRequest('Только DELETE запрос')

# Создание нового посещения
@csrf_exempt
def visit_create(request):
    if(request.method == 'POST'):
        data = parse_json(request)
        if not data:
            return HttpResponseBadRequest('Ошибка парсинга JSON')
        user = get_object_or_404(User, card_id=data.get('card_id'))
        # разбор visited_at если передана строка в ISO формате
        visited = data.get('visited_at', None)
        if visited:
            try:
                dt = datetime.fromisoformat(visited)
                if dt.tzinfo is None:
                    dt = timezone.make_aware(dt, timezone.get_current_timezone())
                visited_at = dt
            except Exception:
                visited_at = timezone.now()
        else:
            visited_at = timezone.now()

        visit = Visit.objects.create(
            user=user,
            visited_at=visited_at
        )
        return JsonResponse({ 'user_id': str(visit.user.id), 'visited_at': visit.visited_at.isoformat() })
    return HttpResponseBadRequest('Только POST запрос.')

# Получение списка всех посещений
@csrf_exempt
def visit_list_all(request):
    if request.method != 'GET':
       visits = Visit.objects.select_related('user').all().order_by('-visited_at')
       visits_list = []
       for visit in visits:
           visits_list.append({
               'id': visit.id,
               'user_id': str(visit.user.id),
               'user_td_username': visit.user.td_username,
               'user_fullname': visit.user.fullname,
               'visited_at': visit.visited_at.isoformat()
           })
       return JsonResponse(visits_list, safe=False)
    return HttpResponseBadRequest('Только GET запрос')

# Получение списка посещений по user_id
@csrf_exempt
def visit_list_by_user(request, user_id):
    if request.method != 'GET':
        return HttpResponseBadRequest('Только GET запрос')
    if not User.objects.filter(id=user_id).exists():
        return HttpResponseBadRequest('Пользователь не найден')
    visits = Visit.objects.filter(user_id=user_id).order_by('-visited_at')
    result = [{
        'id': v.id,
        'visited_at': v.visited_at.isoformat()
    } for v in visits]
    return JsonResponse(result, safe=False)   

# Получение fullname по td_username
@csrf_exempt
def getname(request, tg_username):
    if request.method != 'GET':
        return HttpResponseBadRequest('Только GET запрос')
    user = User.objects.filter(td_username=tg_username).first()
    if user:
        return JsonResponse({'fullname': user.fullname})
    else:
        return HttpResponseBadRequest('Пользователь не найден')

# Получение списка посещений за указанный месяц и год, с опциональной фильтрацией по user_id
@csrf_exempt
def visit_list_month(request):
    """
    GET /api/visits/month/?year=2025&month=10[&user_id=<id>]
    Возвращает все посещения в указанном месяце (период: >= first_day, < next_month_first_day).
    Если year/month не указаны — берётся текущий месяц.
    Опционально: user_id для фильтрации по пользователю.
    """
    if request.method != 'GET':
        return HttpResponseBadRequest('Только GET запрос')

    tz = timezone.get_current_timezone()
    now = timezone.now()

    # получение года и месяца из query params
    try:
        year = int(request.GET.get('year', now.year))
        month = int(request.GET.get('month', now.month))
        if not (1 <= month <= 12):
            raise ValueError
    except ValueError:
        return HttpResponseBadRequest('Некорректные параметры year или month')

    # вычисляем границы диапазона [start, end)
    start = datetime(year, month, 1, tzinfo=tz)
    # следующий месяц
    if month == 12:
        next_month = datetime(year + 1, 1, 1, tzinfo=tz)
    else:
        next_month = datetime(year, month + 1, 1, tzinfo=tz)

    qs = Visit.objects.select_related('user').filter(visited_at__gte=start, visited_at__lt=next_month).order_by('-visited_at')

    user_id = request.GET.get('user_id')
    if user_id:
        qs = qs.filter(user_id=user_id)

    result = []
    for v in qs:
        result.append({
            'id': v.id,
            'user_id': str(v.user.id),
            'user_td_username': v.user.td_username,
            'user_fullname': v.user.fullname,
            'visited_at': v.visited_at.isoformat()
        })

    return JsonResponse(result, safe=False)

# Удаление посещения
@csrf_exempt
def visit_delete(request, visit_id):
    visit = get_object_or_404(Visit, pk=visit_id)
    if request.method == 'DELETE':
        visit.delete()
        return JsonResponse({'status': 'success'})
    return HttpResponseBadRequest('Только DELETE запрос.')
