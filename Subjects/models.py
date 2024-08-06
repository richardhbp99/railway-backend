from django.db import models

# Create your models here.
class Subject(models.Model):
    id_subject = models.AutoField(primary_key=True, editable=False)
    code = models.CharField(max_length=10, unique=True) 
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey('Teachers.Teacher', on_delete=models.CASCADE)
    prerequisites = models.ManyToManyField('self', symmetrical=False, related_name='prerequisite_subjects', blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"
    
    class Meta:
        db_table = 'T401Subject'
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'


class Enrollment(models.Model):
    id_enrollment = models.AutoField(primary_key=True, editable=False)
    student = models.ForeignKey('Students.Student', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    grade = models.FloatField(null=True)

    class Meta:
        db_table = 'T402Enrollment' 
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'

    def __str__(self):
        return f"{self.student.person} - {self.subject.name}"
    


class Pensum(models.Model):
    id_pensum = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()
    subjects = models.ManyToManyField(Subject, related_name='pensums')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'T403Pensum'
        verbose_name = 'Pensum'
        verbose_name_plural = 'Pensums'