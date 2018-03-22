from datetime import datetime
from peewee import *

db = SqliteDatabase('work_log.db')


class CustomModel(Model):
    class Meta:
        database = db


class Employee(CustomModel):
    date_created = DateTimeField(default=datetime.now())
    name = CharField()

    class Meta:
        database = db


class Task(CustomModel):
    task_date = DateTimeField(default=datetime.now())
    title = CharField(unique=True)
    time_spent = TimeField()
    notes = TextField(default='')
    employee = ForeignKeyField(Employee)

    class Meta:
        database = db

def initialize_db():
    db.connect()
    db.create_tables([Employee, Task], safe=True)