from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=255)
    tutor = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    period = models.IntegerField() 
    description = models.TextField()
    total_students = models.IntegerField(default=0) 
    status = models.CharField(
        max_length=20,
        choices=[
            ('open', 'Open for Registration'),
            ('close', 'Closed')
        ],
        default='close'
    )
    
    def __str__(self):
        return self.title
    
class Registration(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="registrations")  
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
    
    def withdraw(self):
        self.delete()

def update_total_students_on_save(sender, instance, created, **kwargs):
    if created: 
        instance.course.total_students = instance.course.registrations.count()
        instance.course.save()

def update_total_students_on_delete(sender, instance, **kwargs):
    instance.course.total_students = instance.course.registrations.count()
    instance.course.save()   
