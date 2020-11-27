from data.config import ADMIN_ID
from utils.db_api.models import Group, User, Links, db


def initialize_db():
    db.connect()
    db.create_tables([
        Group,
        User,
        Links
    ], safe=True)
    admin_group, created = Group.get_or_create(group_name='Admins')
    user_group, created = Group.get_or_create(group_name='Users')
    Group.get_or_create(group_name='Unauthorized')
    Group.get_or_create(group_name='Zavhoz')
    Group.get_or_create(group_name='SysAdmins')
    Group.get_or_create(group_name='Inventarization')
    root, created = User.get_or_create(telegram_id=ADMIN_ID,
                                       first_name='Dzen',
                                       last_name='Bots',
                                       username='DzenBots',
                                       status='')
    Links.get_or_create(user=root,
                        group=admin_group)
    Links.get_or_create(user=root,
                        group=user_group)

