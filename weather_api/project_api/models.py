import uuid as uuid
from django.db import models
import jsonfield
from django.utils.translation import ugettext_lazy as _

from user.models import User


class BaseModel(models.Model):
    """parent model which will be inherited by all other child models"""

    modified_on = models.DateTimeField(auto_now=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        abstract = True


class CityWeatherCollection(BaseModel):
    """City-weather model"""
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    city = models.CharField(max_length=100, default='')
    current_temp = models.CharField(max_length=100, default='')
    feels_like_temp = models.CharField(max_length=100, default='')

    class Meta:
        db_table = 'city_weather_collection'
        verbose_name = _('City Weather Collection')
        verbose_name_plural = _('City Weather Collections')

    def __str__(self):
        return self.uuid.__str__()


class MailingTask(BaseModel):
    """Email task model."""
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    emails = jsonfield.JSONField(default=list)
    status = models.CharField(max_length=100, default='pending')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_collections')

    class Meta:
        db_table = 'mailing_task'
        verbose_name = _('Mailing Task')
        verbose_name_plural = _('Mailing Tasks')

    def __str__(self):
        return self.uuid.__str__()
