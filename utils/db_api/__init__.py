from utils.db_api.models import Group, User, Links, db


def initialize_db():
    db.connect()
    db.create_tables([
        Group,
        User,
        Links
    ], safe=True)
    Group.get_or_create(group_name='Admins')
    Group.get_or_create(group_name='Users')
    Group.get_or_create(group_name='Unauthorized')
