def make_sets(sets: dict):
    """Формирует словарь сетов с количеством и общей ценой."""
    total_price = 0
    for item in sets:
        if item in range(1, 4):
            price = 400
        elif item in range(4, 7):
            price = 500
        else:
            price = 700
        total_price += sets[item] * price
    data = {'total_price': total_price}
    sets.update(data)
    return sets
