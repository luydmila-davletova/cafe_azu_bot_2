import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect

from cafe.models import Cafe

from .forms import BookingForm, ComboForm, DishesForm, LocationForm
from .models import OrderSets, Reservation


@csrf_protect
def index(request):
    response_data = {
        'app_name': 'AzuBot',
    }
    return JsonResponse(response_data)


@csrf_protect
def book_table(request):
    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            date = booking_form.cleaned_data.get('date')
            cafe = booking_form.cleaned_data.get('cafe')
            name = booking_form.cleaned_data.get('name')
            number = booking_form.cleaned_data.get('number')
            set_instance = booking_form.cleaned_data.get('set')
            quantity = booking_form.cleaned_data.get('quantity')
            if set_instance and set_instance.price >= 0 and quantity > 0:
                booking = Reservation.objects.create(
                    date=date,
                    cafe=cafe,
                    name=name,
                    number=number,
                    status='booked')
                order_sets = OrderSets(
                    reservation=booking,
                    sets=set_instance,
                    quantity=quantity)
                order_sets.save()
                response_data = {
                    'status': 'success',
                    'message': booking.id,
                }
            else:
                response_data = {
                    'status': 'error',
                    'message': 'Ошибка меню или его количества.',
                }
        else:
            response_data = {
                'status': 'error',
                'message': 'Ошибка данных.',
            }
    else:
        response_data = {
            'status': 'error',
            'message': 'Неверный метод запроса.',
        }
    return JsonResponse(response_data)


@csrf_protect
def create_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            location = Cafe(name=name, address=address)
            location.save()
            response_data = {
                'status': 'success',
                'message': 'Создано',
            }
        else:
            response_data = {
                'status': 'error',
                'message': 'Ошибка данных.',
            }
    else:
        response_data = {
            'status': 'error',
            'message': 'Неверный метод запроса.',
        }
    return JsonResponse(response_data)


@csrf_protect
def update_location(request, location_id):
    location = get_object_or_404(Cafe, id=location_id)
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            response_data = {
                'status': 'success',
                'message': 'Адрес успешно обновлен',
            }
        else:
            response_data = {
                'status': 'error',
                'message': 'Ошибка данных.',
            }
    else:
        response_data = {
            'status': 'error',
            'message': 'Неверный метод запроса.',
        }
    return JsonResponse(response_data)


@csrf_protect
def delete_location(request, location_id):
    location = get_object_or_404(Cafe, id=location_id)
    if request.method == 'POST':
        if location:
            location.delete()
            response_data = {
                'status': 'success',
                'message': 'Адрес успешно удален',
            }
        else:
            response_data = {
                'status': 'error',
                'message': 'Адрес не найден.',
            }
    else:
        response_data = {
            'status': 'error',
            'message': 'Неверный метод запроса.',
        }
    return JsonResponse(response_data)


@csrf_protect
def update_booking(request, booking_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            payment_status = data.get('payment_status')
            if payment_status is not None:
                booking = Reservation.objects.get(pk=booking_id)
                booking.payment_status = payment_status
                booking.save()
                response_data = {
                    'status': 'success',
                    'message': 'Бронирование успешно обновлено.',
                }
            else:
                response_data = {
                    'status': 'error',
                    'message': 'Требуется оплата.',
                }
        except json.JSONDecodeError:
            response_data = {
                'status': 'error',
                'message': 'Ошибка JSON.',
            }
        except Reservation.DoesNotExist:
            response_data = {
                'status': 'error',
                'message': 'Бронирование не найдено.',
            }
    else:
        response_data = {
            'status': 'error',
            'message': 'Неверный метод запроса.',
        }
    return JsonResponse(response_data)


@csrf_protect
def create_combo(request):
    if request.method == 'POST':
        form = ComboForm(request.POST)
        if form.is_valid():
            form.save()
            response_data = {
                'status': 'success',
                'message': 'Комбо-сет создан успешно',
            }
        else:
            response_data = {
                'status': 'error',
                'errors': form.errors,
            }
    else:
        response_data = {
            'status': 'error',
            'message': 'Неверный метод запроса.',
        }
    return JsonResponse(response_data)


@csrf_protect
def create_dish(request):
    if request.method == 'POST':
        form = DishesForm(request.POST)
        if form.is_valid():
            form.save()
            response_data = {
                'status': 'success',
                'message': 'Блюдо успешно создано',
            }
        else:
            response_data = {
                'status': 'error',
                'message': 'Ошибка данных.',
            }
    else:
        response_data = {
            'status': 'error',
            'message': 'Неверный метод запроса.',
        }
    return JsonResponse(response_data)
