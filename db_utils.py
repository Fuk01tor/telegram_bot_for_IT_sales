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
    return db.Users.hgetall(user_id)
