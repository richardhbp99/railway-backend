from django.db import models

# Create your models here.
class Person(models.Model):
    id_person = models.AutoField(primary_key=True, editable=False)
    names = models.CharField(max_length=200, null=False)
    last_names = models.CharField(max_length=200, null=False)
    identification_number = models.CharField(max_length=50, unique=True, blank=False, null=False)
    email = models.EmailField(max_length=254, unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    class Meta:
        db_table = 'T101Person'
        verbose_name = 'Person'
        verbose_name_plural = 'People'

    def __str__(self):
        return f"{self.names} {self.last_names} ({self.identification_number}, {self.email}, {self.phone_number})"