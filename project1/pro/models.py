from distutils import errors
from django.db import models

# Create your models here.

class CategoryManager(models.Manager):
    def category_validator(self, postData):
        errors = {}

        if len(postData['name']) < 1:
            errors['name'] = "Name of category must be provided"

class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category_creator = models.ForeignKey(User,related_name="categories_mader",on_delete=models.CASCADE)
    objects = CategoryManager()


class CourseManager(models.Manager):
    def course_validator(self, postData):
        errors = {}

        if len(postData['name']) < 1:
            errors['name'] = "Name of the course must be provided"
        if len(postData['description']) < 3:
            errors['description'] = "Description must be at least 3 characters"
        if len(postData['instructor']) < 1:
            errors['instructor'] = "instructor name must be provided"
        if len(postData['goals']) < 1:
            errors['goals'] = "Goals of the course must be provided"

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.CharField(max_length=255)
    goals = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category,related_name='courses')
    course_creator = models.ForeignKey(User,related_name="courses_mader",on_delete=models.CASCADE)
    objects = CourseManager()

class SectionManager(models.Manager):
    def section_validator(self, postData):
        if len(postData['name']) < 1:
            errors['name'] = "Name of the course must be provided"
        if len(postData['description']) < 3:
            errors['description'] = "Description must be at least 4 characters"


class Section(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    course = models.ForeignKey(Course, related_name="sections",on_delete=models.CASCADE)
    section_creator = models.ForeignKey(User,related_name="sections_mader",on_delete=models.CASCADE)
    objects = SectionManager()

class SubjectManager(models.Manager):
    def subject_validator(self, postData):
        if len(postData['title']) < 1:
            errors['title'] = "Name of the course must be provided"

class Subject(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    section = models.ForeignKey(Section,related_name="subjects",on_delete=models.CASCADE)
    subject_creator = models.ForeignKey(User,related_name="subjects_mader",on_delete=models.CASCADE)
    objects = SubjectManager()