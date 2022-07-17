from django.db import models
import re
import bcrypt
import datetime

class UserManager(models.Manager):
    def register_validation(self,postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name must be more than 2 characters "

        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name must be more than 2 characters "

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email is not valid"
        else:
            try:
                user = User.objects.get(email__iexact=postData['email'])
                errors['email'] = "Email is already registered try to login!"  
            except:
                pass
        
        if postData['date_of_birth']:
            birthday = datetime.datetime.strptime(postData['date_of_birth'],"%Y-%m-%d") # convert the string date into datetime type
            _birthday = datetime.datetime.today() - birthday # substract today date from the birthday given a timedelta type
            if birthday > datetime.datetime.today():
                errors['date_of_birth'] = "Date of Birth should be in the past !"
            elif _birthday.days > 365 * 18: # compare number of days in the DoB with 18years days .
                errors['date_of_birth'] = "max age is 18 :) "
        else:
            errors['date_of_birth'] = "date of birth is required"

        if postData['password'] != postData['confirm_password']:
            errors["passwords"] = "passwords are not matched!" 

        if len(postData['password']) < 8:
            errors["password"] = "password should be at least 8 characters" 
        
        return errors

    def login_validation(self,postData):
        errors = {}

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email is not valid"
        else:
            try:
                user = User.objects.get(email__iexact=postData['email'])
                if not bcrypt.checkpw(postData['password'].encode(),user.password.encode()):
                    errors['login'] = "Email or Password is incorrect !"
            except:
                errors['login'] = "Email or Password is incorrect !"
        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    date_of_birth = models.DateTimeField()
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category_creator = models.ForeignKey(User,related_name="categories_mader",on_delete=models.CASCADE)

class Course(models.Model):
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.CharField(max_length=255)
    goals = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category,related_name='courses')
    course_creator = models.ForeignKey(User,related_name="courses_mader",on_delete=models.CASCADE)

class Section(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    course = models.ForeignKey(Course, related_name="sections",on_delete=models.CASCADE)
    section_creator = models.ForeignKey(User,related_name="sections_mader",on_delete=models.CASCADE)

class Subject(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    section = models.ForeignKey(Section,related_name="subjects",on_delete=models.CASCADE)
    subject_creator = models.ForeignKey(User,related_name="subjects_mader",on_delete=models.CASCADE)


    









    



