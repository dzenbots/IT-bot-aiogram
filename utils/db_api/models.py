from peewee import CharField, ForeignKeyField, SqliteDatabase, Model

from data.config import DB_FILE_PATH

db = SqliteDatabase(DB_FILE_PATH, pragmas={'foreign_keys: 1'})


class BaseModel(Model):
    class Meta:
        database = db


class Group(BaseModel):
    group_name = CharField(unique=True)


class User(BaseModel):
    telegram_id = CharField(unique=True)
    first_name = CharField()
    last_name = CharField()
    nickname = CharField()
    status = CharField()


class Links(BaseModel):
    user = ForeignKeyField(User, backref='links')
    group = ForeignKeyField(Group, backref='links')
