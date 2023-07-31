
from django.db import models
from django.contrib.auth.models import AbstractUser, User, AbstractBaseUser,  BaseUserManager, PermissionsMixin
from cloudinary.models import CloudinaryField
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


def get_default_image():
    return 'profile/default.png'


class StudentManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        username = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.create_user(username, password=password, **extra_fields)
        user.is_admin = True
        user.save(using=self._db)
        return user
        

      

class Student(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100,unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100)
    program = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='profile/', default=get_default_image, null=True, blank=True)
    room = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = StudentManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.id



    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



class Hall(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    image = models.ImageField(upload_to='hall/image/',null=True, blank=True)


    def __str__(self):
        return self.name
    

class HallImage(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hall/carousel/', null=True, blank=True)

    def __str__(self):
        return f"Image for {self.hall.name}"


class Room(models.Model):
    room_type = (("Flat","Flat"),("4 in 1","4 in 1"))
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    room_number = models.PositiveIntegerField()
    type = models.CharField(choices=room_type, max_length=20, default='4 in 1')
    occupants = models.PositiveIntegerField(default=0)
    floor = models.PositiveIntegerField()
    price = models.PositiveIntegerField(default=1200)

    def __str__(self):
        return str(self.room_number) + " " + str(self.hall)
    
    

class Booking(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE,null=True)
    date = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    

    def __str__(self):
        return str(self.student.name) + " " + str(self.room) + " " + str(self.date) + " " + str(self.room.hall)
    


class HallManager(models.Model):
    first_name = models.CharField(max_length=50, null=True)
    last_name= models.CharField(max_length=50, null=True)
    manager_ID = models.CharField(max_length=50 , null=True)
    manager_contact = models.CharField(max_length=100 , null=True)
    manager_email = models.EmailField(max_length=100 , null=True)
    position = models.CharField(max_length=20 , null=True)
    password = models.CharField(max_length=100 , null=True)
    hall = models.ForeignKey(Hall, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Hall Manager: {self.first_name} {self.last_name} {self.manager_contact} {self.position}'
    

class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return self.value + " " + str(self.date) + " " + str(self.student) + " " + str(self.room)
    

    @staticmethod
    def delete_expired_messages():
        Message.objects.filter(date__lt=timezone.now() - timedelta(minutes=2)).delete()

def delete_expired_messages(sender,instance,**kwargs):
    Message.objects.filter(date__lt=timezone.now() - timedelta(minutes=1)).delete()

pre_save.connect(delete_expired_messages, sender=Message)