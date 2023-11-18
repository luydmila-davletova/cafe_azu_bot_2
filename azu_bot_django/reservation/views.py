import json

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_protect

from cafe.models import Cafe
from menu.models import Set
from tables.models import Table

from .forms import BookingForm, ComboForm, DishesForm, LocationForm, TableForm
from .models import OrderSets, Reservation, TableReservation


@csrf_protect
def index(request):
    context = {
        'app_name': 'AzuBot',
    }
    return render(request, 'index.html', context)


@csrf_protect
@transaction.atomic
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
            if quantity == 1:
                available_bar_tables = Table.objects.select_for_update(
                ).filter(
                    cafe__id=cafe.id,
                    table_type='bar_table',
                ).exclude(
                    table_reservations__reservation__date=date,
                    table_reservations__reservation__status='booked'
                )
                bar_table = available_bar_tables.filter(
                    quantity__gte=1).first()
                if bar_table:
                    reservation = Reservation.objects.create(
                        date=date,
                        cafe=cafe,
                        name=name,
                        number=number,
                        status='booked'
                    )
                    TableReservation.objects.create(
                        table=bar_table,
                        reservation=reservation,
                        quantity=1
                    )
                    order_sets = OrderSets(
                        reservation=reservation,
                        sets=set_instance,
                        quantity=1
                    )
                    order_sets.save()
                    return JsonResponse({
                        'status': 'success',
                        'message': reservation.id,
                        'bookings': list(Reservation.objects.values())
                    })
            available_simple_tables = Table.objects.select_for_update().filter(
                cafe__id=cafe.id,
                table_type='simple_table',
            ).exclude(
                table_reservations__reservation__date=date,
                table_reservations__reservation__status='booked'
            )
            available_bar_tables = Table.objects.select_for_update().filter(
                cafe__id=cafe.id,
                table_type='bar_table',
            ).exclude(
                table_reservations__reservation__date=date,
                table_reservations__reservation__status='booked'
            )
            single_table = available_simple_tables.filter(
                quantity__gte=quantity).first()
            if single_table:
                reservation = Reservation.objects.create(
                    date=date,
                    cafe=cafe,
                    name=name,
                    number=number,
                    status='booked'
                )
                TableReservation.objects.create(
                    table=single_table,
                    reservation=reservation,
                    quantity=quantity
                )
                order_sets = OrderSets(
                    reservation=reservation,
                    sets=set_instance,
                    quantity=quantity
                )
                order_sets.save()
                return JsonResponse({
                    'status': 'success',
                    'message': reservation.id,
                    'bookings': list(Reservation.objects.values())
                })
            else:
                merged_tables = merge_tables(available_simple_tables, quantity)
                if merged_tables:
                    reservation = Reservation.objects.create(
                        date=date,
                        cafe=cafe,
                        name=name,
                        number=number,
                        status='booked'
                    )
                    for table in merged_tables:
                        TableReservation.objects.create(
                            table=table,
                            reservation=reservation,
                            quantity=table.quantity
                        )
                        quantity -= table.quantity
                    order_sets = OrderSets(
                        reservation=reservation,
                        sets=set_instance,
                        quantity=quantity
                    )
                    order_sets.save()
                    return JsonResponse({
                        'status': 'success',
                        'message': reservation.id,
                        'bookings': list(Reservation.objects.values())
                    })
                else:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Недостаточно свободных столов.'
                    })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Ошибка заполнения.'
            })
    else:
        booking_form = BookingForm()
        return JsonResponse({
            'booking_form': booking_form,
            'bookings': list(Reservation.objects.values())
        })


def merge_tables(available_tables, required_quantity):
    available_tables = available_tables.order_by('-quantity')
    merged_tables = []
    total_quantity = 0
    for table in available_tables:
        merged_tables.append(table)
        total_quantity += table.quantity
        if total_quantity >= required_quantity:
            return merged_tables
    return None


def make_reservation_after_merge(merged_tables, date, cafe,
                                 name, number, set_instance,
                                 quantity):
    reservation = Reservation.objects.create(
        date=date,
        cafe=cafe,
        name=name,
        number=number,
        status='booked'
    )
    for table in merged_tables:
        TableReservation.objects.create(
            table=table,
            reservation=reservation,
            quantity=table.quantity
        )
        quantity -= table.quantity
    order_sets = OrderSets(
        reservation=reservation,
        sets=set_instance,
        quantity=quantity
    )
    order_sets.save()
    return reservation.id


@csrf_protect
def create_location(request):
    existing_locations = Cafe.objects.all()
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            location = Cafe(name=name, address=address)
            location.save()
            return JsonResponse({'message': 'Создано'})
        else:
            return JsonResponse({'status': 'error',
                                 'message': 'Ошибка данных.'})
    else:
        form = LocationForm()
    context = {
        'form': form,
        'existing_locations': list(existing_locations.values()),
    }
    return JsonResponse(context)


@csrf_protect
def update_location(request, location_id):
    location = get_object_or_404(Cafe, id=location_id)
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success',
                                 'message': 'Адрес успешно обновлен'})
        else:
            return JsonResponse({'status': 'error',
                                 'message': 'Ошибка данных.'})
    else:
        form = LocationForm(instance=location)
        context = {
            'form': form,
            'location': list(location.values())
        }
    return JsonResponse(context)


@csrf_protect
def delete_location(request, location_id):
    location = get_object_or_404(Cafe, id=location_id)
    if request.method == 'POST':
        if location:
            location.delete()
            return JsonResponse({'status': 'success',
                                 'message': 'Адрес успешно удален'})
        else:
            return JsonResponse({'status': 'error',
                                 'message': 'Адрес не найден.'})
    else:
        return JsonResponse({'status': 'error',
                             'message': 'Неверный метод запроса.'})


@csrf_protect
def update_booking(request, booking_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            payment_status = data.get('payment_status')
            if payment_status is None:
                return JsonResponse({'error': 'Требуется оплата.'}, status=400)
            booking = Reservation.objects.get(pk=booking_id)
            booking.payment_status = payment_status
            booking.save()
            return JsonResponse({'message': 'Бронирование успешно обновлено.'},
                                status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Ошибка JSON.'}, status=400)
        except Reservation.DoesNotExist:
            return JsonResponse({'error': 'Бронирование не найдено.'},
                                status=404)
    else:
        return JsonResponse({'error': 'Неверный метод запроса.'}, status=405)


@csrf_protect
def create_combo(request):
    combos = Set.objects.all()
    if request.method == 'POST':
        form = ComboForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success',
                                 'message': 'Комбо-сет успешно создан'})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'status': 'error',
                                 'errors': errors}, status=400)
    else:
        form = ComboForm()
    context = {
        'form': form,
        'combos': list(combos.values()),
    }
    return JsonResponse(context)


@csrf_protect
def create_dish(request):
    if request.method == 'POST':
        form = DishesForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success',
                                 'message': 'Блюдо успешно создано'})
    else:
        form = DishesForm()
    context = {'form': form}
    return JsonResponse(context)


@csrf_protect
def create_table(request):
    if request.method == 'POST':
        table_form = TableForm(request.POST)
        if table_form.is_valid():
            name = table_form.cleaned_data.get('name')
            cafe = table_form.cleaned_data.get('cafe')
            capacity = table_form.cleaned_data.get('quantity')
            table_type = table_form.cleaned_data.get('table_type')
            if table_type == 'simple_table':
                Table.objects.create(name=name,
                                     cafe=cafe,
                                     quantity=capacity,
                                     table_type='simple_table')
            elif table_type == 'bar_table':
                Table.objects.create(name=name,
                                     cafe=cafe,
                                     quantity=capacity,
                                     table_type='bar_table')
            return JsonResponse({'status': 'success',
                                 'message': 'Стол успешно создан'})
        else:
            return JsonResponse({'status': 'error',
                                 'message': 'Ошибка данных.'})
    else:
        table_form = TableForm()
    context = {'table_form': table_form}
    return JsonResponse(context)
