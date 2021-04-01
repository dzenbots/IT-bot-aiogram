from data.config import ADMIN_ID
from .models import Group, User, Links, db, Equipment, Movement, Person


def initialize_db():
    db.connect()
    db.create_tables([
        Group,
        User,
        Links,
        Equipment,
        Movement,
        Person
    ], safe=True)
    admin_group, created = Group.get_or_create(group_name='Admins')
    user_group, created = Group.get_or_create(group_name='Users')
    Group.get_or_create(group_name='Unauthorized')
    Group.get_or_create(group_name='Zavhoz')
    Group.get_or_create(group_name='SysAdmins')
    Group.get_or_create(group_name='Inventarization')
    Group.get_or_create(group_name='PhonesAdmin')
    Group.get_or_create(group_name='SiteAdmin')
    root, created = User.get_or_create(telegram_id=ADMIN_ID,
                                       defaults={
                                           'first_name': 'Dzen',
                                           'last_name': 'Bots',
                                           'username': 'DzenBots',
                                           'status': ''})
    Links.get_or_create(user=root,
                        group=admin_group)
    Links.get_or_create(user=root,
                        group=user_group)
