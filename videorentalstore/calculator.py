def calculate_price(days, category):
    if days >= 0:
        premium_price = 40
        basic_price = 30
        price = 0

        if category == 'regular film':
            if days <= 3:
                return basic_price
            else:
                extra_days = days - 3
                price = basic_price + (extra_days * basic_price)
                return price
        elif category == 'old film':
            if days <= 5:
                return basic_price
            else:
                extra_days = days - 5
                price = basic_price + (extra_days * basic_price)
                return price
        else:
            price = premium_price * days
            return price
    else:
        return "The days must be greater than or equal to 0"

def calculate_late_charge(overdue_days, category):
    premium_price = 40
    basic_price = 30
    late_charge = 0

    if category == 'new release':
        late_charge = premium_price * overdue_days
        return late_charge
    elif category == 'regular film':
        late_charge = basic_price * overdue_days
        return late_charge
    else:
        late_charge = basic_price * overdue_days
        return late_charge

def calculate_bonus_point(category):
    if category == 'new release':
        return 2
    else:
        return 1