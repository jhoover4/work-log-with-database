from datetime import datetime
from peewee import *

db = SqliteDatabase('work_log.db')


class Employee(Model):
    date_created = DateTimeField(default=datetime.now())
    name = CharField()

    class Meta:
        database = db


class Task(Model):
    task_date = DateTimeField(default=datetime.now())
    title = CharField(unique=True)
    time_spent = TimeField()
    notes = TextField()
    employee = ForeignKeyField(Employee)

    class Meta:
        database = db
