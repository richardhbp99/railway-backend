from django.db import models

# Create your models here.
class Teacher(models.Model):
    id_teacher = models.AutoField(primary_key=True, editable=False)
    person = models.OneToOneField('Security.Person', on_delete=models.CASCADE)
   
    class Meta:
        db_table = 'T301Teacher'
