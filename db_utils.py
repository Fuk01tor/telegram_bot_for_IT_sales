import db_clients as db


def save_user(message, admin=False):
    user = message.from_user
    db.Users.hmset(user.id, {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'admin': admin,
    })


def get_user(message):
    user_id = message.from_user.id
    user = db.Users.hgetall(user_id)
    user['admin'] = user['admin'] == 'True'
    return user


def get_next_unique_id():
    return db.Monitors.incr('id_counter')


def save_monitor(brand=None, manufacture_year=None, price=None):
    db.Monitors.hmset(get_next_unique_id(), {
        'brand': brand,
        'manufacture_year': manufacture_year,
        'price': price,
    })


def readable_monitor_info(unique_id=None, brand=None,
                          manufacture_year=None, price=None):
    return """{}: Brand: {} Manufacture year: {} Price: {}\n""".format(
        unique_id, brand, manufacture_year, price)


def get_monitors():
    result = ''
    for key in db.Monitors.scan_iter():
        if (key == 'id_counter'):
            continue
        values = db.Monitors.hgetall(key)
        result += readable_monitor_info(
            unique_id=key,
            brand=values['brand'],
            manufacture_year=values['manufacture_year'],
            price=values['price'])
    return result


def remove_monitor(unique_id):
    if (not db.Monitors.exists(unique_id)):
        raise Exception('{} does not exist in the stock'.format(unique_id))
    db.Monitors.delete(unique_id)
