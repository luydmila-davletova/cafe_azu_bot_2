from handlers.api import post_quantity


async def get_free_places(cafes, context_data):
    """Получить количество свободных мест в кафе."""
    avaliable_cafes = []
    person_amount = int(context_data.get('person_amount'))
    for cafe in cafes:
        if cafe['address'] == context_data.get('address'):
            del cafe
        else:
            data_dict = {}
            data_dict['date'] = '-'.join(
                context_data.get('date').split('.')[::-1]
            )
            data_dict['quantity'] = 0
            check_current_cafe = await post_quantity(
                cafe['id'], data=data_dict
            )
            free_places = int(check_current_cafe['quantity'])
            if person_amount <= free_places:
                avaliable_cafes.append(cafe['address'])
            else:
                del cafe
    return avaliable_cafes
