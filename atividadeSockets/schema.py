import datetime
import peewee


class BaseModel(peewee.Model):
    class Meta:
        database = None


class Directors(BaseModel):
    name = peewee.CharField()

    created_at = peewee.DateTimeField(default=datetime.datetime.now)
    updated_at = peewee.DateTimeField()

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super().save(*args, **kwargs)


class Movies(BaseModel):
    title = peewee.CharField()
    director = peewee.ForeignKeyField(Directors, backref="movies")
    rating = peewee.FloatField(default=0.0)
    duration_min = peewee.IntegerField(default=0)

    created_at = peewee.DateTimeField(default=datetime.datetime.now)
    updated_at = peewee.DateTimeField()
