from mongoengine.connection import get_db


def _config():
    return get_db().certuk_config


def save(name, value):
    _config().update({
        'name': name
    }, value, True)


def get(name):
    return _config().find_one({
        'name': name
    }, {'_id': False})


def get_all():
    cursor = _config().find({}, {
        '_id': 0
    })
    results = {}
    for doc in cursor:
        results[doc["name"]] = doc

    return results
