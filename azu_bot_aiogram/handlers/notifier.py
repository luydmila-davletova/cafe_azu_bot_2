from aiogram import types
from aiogram.fsm.context import FSMContext


@dp.message_handler(state="*")
async def process_booking(message: types.Message, state: FSMContext):
    date = state.get('date')
    cafe = state.get('cafe')
    name = state.get('name')
    number = state.get('number')
    set_instance = state.get('set')
    quantity = state.get('quantity')
    booking = Reservation.objects.create(
        date=date,
        cafe=cafe,
        name=name,
        number=number,
        status='booked'
    )
    order_sets = OrderSets(
        reservation=booking,
        sets=set_instance,
        quantity=quantity
    )
    order_sets.save()

    admin_message = f"Новое бронирование!\n\nДата: {date}\nИмя: {name}\nНомер телефона: {number}\nКафе: {cafe}\n"
    await send_notification(admin_message)

    await message.answer("Спасибо за бронирование! Администратор был уведомлен.")
    await state.finish()
