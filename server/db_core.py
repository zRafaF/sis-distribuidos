import peewee
import os
import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
db = peewee.SqliteDatabase(os.path.join(current_dir, "database.db"))


def initialize_db() -> None:
    db.bind([Directors, Movies])
    db.connect()
    db.create_tables([Directors, Movies], safe=True)
    print("Database initialized with Director and Movie tables.")



class BaseModel(peewee.Model):
    class Meta:
        database = None


class Directors(BaseModel):
    name = peewee.CharField()
    age = peewee.IntegerField()

    created_at = peewee.DateTimeField(default=datetime.datetime.now)
    updated_at = peewee.DateTimeField()

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super().save(*args, **kwargs)


class Movies(BaseModel):
    title = peewee.CharField()
    director_id = peewee.ForeignKeyField(Directors, backref="movies")
    rating = peewee.FloatField(default=0.0)
    duration_min = peewee.IntegerField(default=0)
    gender = peewee.CharField(default="Unknown")

    created_at = peewee.DateTimeField(default=datetime.datetime.now)
    updated_at = peewee.DateTimeField()

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super().save(*args, **kwargs)
