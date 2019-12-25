# class Calculator():

def calculate_price(days, category):
    if days >= 1:
        premium_price = 40
        basic_price = 30
        price = 0

        if category == 'new release':
            price = premium_price * days
            return price
        elif category == 'regular film':
            if days <= 3:
                return basic_price
            else:
                extra_days = days - 3
                price = basic_price + (extra_days * basic_price)
                return price
        else:
            if days <= 5:
                return basic_price
            else:
                extra_days = days - 5
                price = basic_price + (extra_days * basic_price)
                return price
    else:
        return "The days must be greater than and equal to 1"

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