from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from django.contrib import messages


def index(request):
    return render(request,'login_register/login_and_registertion.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.register_validation(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request,value)
            return redirect("/") 
        else:
            hash_pass = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
            user = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                date_of_birth = request.POST['date_of_birth'],
                password = hash_pass
            )
            user.save()
            messages.success(request,"User successfully added!")

            request.session['user_id'] = user.id
            return redirect('/home')
    return redirect('/')

def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validation(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request,value)
            return redirect("/")
        else:
            userid = User.objects.get(email__iexact=request.POST['email'])
            request.session['user_id'] = userid.id
            if userid.is_admin:
                return redirect('/home')
            else:
                return redirect('/home')

    return redirect('/') 

def home(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'categories':Category.objects.all(),
        'courses':Course.objects.all(),
    }
    return render(request,'frontend/home.html',context)

def show_course(request,course_id):
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'categories':Category.objects.all(),
        'course':Course.objects.get(id=course_id)
    }
    return render(request,'frontend/show_course.html',context)

def show_subject(request,subject_id):
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'categories':Category.objects.all(),
        'subject':Subject.objects.get(id=subject_id)
    }
    return render(request,'frontend/show_subject.html',context)

def logout(request):
    del request.session['user_id']
    return redirect('/')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    _user = User.objects.get(id=request.session['user_id'])
    if not _user.is_admin:
        return redirect('/home')

    return render(request, 'dashboard/dashboard.html')


# Categories functions #

def all_categories(request):
    if 'user_id' not in request.session:
        return redirect('/dashboard')
    _user = User.objects.get(id=request.session['user_id'])
    if not _user.is_admin:
        return redirect('/home')
    context = {
        'categories': Category.objects.all()
    }
    return render(request, 'dashboard/category/all_categories.html', context)


def new_category(request):
    if 'user_id' not in request.session:
        return redirect('/dashboard')
    _user = User.objects.get(id=request.session['user_id'])
    if not _user.is_admin:
        return redirect('/home')

    return render(request, 'dashboard/category/new_category.html')


def create_category(request):
    if 'user_id' not in request.session:
        return redirect('/dashboard')
    _user = User.objects.get(id=request.session['user_id'])
    if not _user.is_admin:
        return redirect('/success')

    _user = User.objects.get(id=request.session['user_id'])
    create_catgory = Category.objects.create(
        name=request.POST['name'],
        category_creator=_user
    )
    create_catgory.save()
    return redirect('/dashboard/category')


def edit_category(request, category_id):
    if 'user_id' not in request.session:
        return redirect('/dashboard')
    _user = User.objects.get(id=request.session['user_id'])
    if not _user.is_admin:
        return redirect('/home')

    context = {
        'category': Category.objects.get(id=category_id)
    }

    return render(request, 'dashboard/category/edit_category.html',context)


def update_category(request, category_id):
    if 'user_id' not in request.session:
        return redirect('/dashboard')
    _user = User.objects.get(id=request.session['user_id'])
    if not _user.is_admin:
        return redirect('/home')

    category = Category.objects.get(id=category_id)
    category.name=request.POST['name']
    category.save()
    return redirect('/dashboard/category')



def delete_category(request, category_id):
    if 'user_id' not in request.session:
        return redirect('/dashboard')
    _user = User.objects.get(id=request.session['user_id'])
    if not _user.is_admin:
        return redirect('/home')
    _category= Category.objects.get(id=category_id)
    _category.delete()

    return redirect('/dashboard/category')

# End of categories #

# Course functions #


def all_courses(request):
    if 'user_id' not in request.session:
        return redirect('/dashboard')
    _user = User.objects.get(id=request.session['user_id'])
    if not _user.is_admin:
        return redirect('/home')

    context = {
        'courses':Course.objects.all()
    }
    return render(request, 'dashboard/course/all_courses.html',context)


def new_course(request):
    if 'user_id' not in request.session:
        return redirect('/dashboard')
    _user = User.objects.get(id=request.session['user_id'])
    if not _user.is_admin:
        return redirect('/home')

    context = {
        'categories':Category.objects.all()
    }
    return render(request, 'dashboard/course/new_course.html' ,context)


def create_course(request):
    if 'user_id' not in request.session:
        return redirect('/dashboard')
    _user = User.objects.get(id=request.session['user_id'])
    if not _user.is_admin:
        return redirect('/home')

    if request.method == 'POST':
        _user = User.objects.get(id=request.session['user_id'])
        course = Course.objects.create(
            name=request.POST['name'],
            image=request.POST['image'],
            description=request.POST['description'],
            instructor=request.POST['instructor'],
            goals=request.POST['goals'],
            course_creator=_user
        )
        for category_id in request.POST.getlist('category'):
            category = Category.objects.get(id=category_id)
            course.categories.add(category)
        
        course.save()
        return redirect('/dashboard/course')



def edit_course(request, course_id):
    if 'user_id' not in request.session:
        return redirect('/dashboard')
    _user = User.objects.get(id=request.session['user_id'])
    if not _user.is_admin:
        return redirect('/home')

    context = {
        'course':Course.objects.get(id=course_id)
    }

    return render(request,'dashboard/course/edit_course.html',context)


def update_course(request, course_id):
    if 'user_id' not in request.session:
        return redirect('/dashboard')
    _user = User.objects.get(id=request.session['user_id'])
    if not _user.is_admin:
        return redirect('/home')

    if request.method=="POST":
        _course=Course.objects.get(id=course_id)
        _course.name=request.POST['name']
        _course.image=request.POST['image']
        _course.description=request.POST['description']
        _course.instructor=request.POST['instructor']
        _course.goals=request.POST['goals']
        _course.save()
    return redirect('/dashboard/course')


def delete_course(request, course_id):
    if 'user_id' not in request.session:
        return redirect('/dashboard')
    _user = User.objects.get(id=request.session['user_id'])
    if not _user.is_admin:
        return redirect('/home')

    _course = Course.objects.get(id=course_id)
    _course.delete()
    return redirect('/dashboard/course')

# End of courses #

# Section functions #


def all_sections(request):
    if 'user_id' not in request.session:
        return redirect('/dashboard')
    _user = User.objects.get(id=request.session['user_id'])
    if not _user.is_admin:
        return redirect('/home')

    context = {
        'sections':Section.objects.all()
    }
    return render(request, 'dashboard/section/all_sections.html',context)


def new_section(request):
    if 'user_id' not in request.session:
        return redirect('/dashboard')
    _user = User.objects.get(id=request.session['user_id'])
    if not _user.is_admin:
        return redirect('/home')
        
    context = {
        'courses':Course.objects.all()
    }
    return render(request, 'dashboard/section/new_section.html',context)


def create_section(request):
    if 'user_id' not in request.session:
        return redirect('/dashboard')
    _user = User.objects.get(id=request.session['user_id'])
    if not _user.is_admin:
        return redirect('/home')

    if request.method == 'POST':
        _user = User.objects.get(id=request.session['user_id'])
        section = Section.objects.create(
            name=request.POST['name'],
            description=request.POST['description'],
            course = Course.objects.get(id=request.POST['course']),
            section_creator = _user
        )
        section.save()
        return redirect('/dashboard/section')


def edit_section(request, section_id):
    if 'user_id' not in request.session:
        return redirect('/dashboard')
    _user = User.objects.get(id=request.session['user_id'])
    if not _user.is_admin:
        return redirect('/home')

    context = {
        'section':Section.objects.get(id=section_id)
    } 
    return render(request,'dashboard/section/edit_section.html',context)


def update_section(request, section_id):
    if 'user_id' not in request.session:
        return redirect('/dashboard')
    _user = User.objects.get(id=request.session['user_id'])
    if not _user.is_admin:
        return redirect('/home')
    
    if request.method == 'POST':
        section = Section.objects.get(id=section_id)
        section.name = request.POST['name']
        section.description = request.POST['description']
        section.save()
        return redirect('/dashboard/section')


def delete_section(request, section_id):
    if 'user_id' not in request.session:
        return redirect('/dashboard')
    _user = User.objects.get(id=request.session['user_id'])
    if not _user.is_admin:
        return redirect('/home')

    section = Section.objects.get(id=section_id)
    section.delete()
    return redirect('/dashboard/section')

# End of sections #

# Subject functions #


def all_subjects(request):
    if 'user_id' not in request.session:
        return redirect('/dashboard')
    _user = User.objects.get(id=request.session['user_id'])
    if not _user.is_admin:
        return redirect('/home')

    context = {
        'subjects':Subject.objects.all()
    }
    return render(request, 'dashboard/subject/all_subjects.html',context)


def new_subject(request):
    if 'user_id' not in request.session:
        return redirect('/dashboard')
    _user = User.objects.get(id=request.session['user_id'])
    if not _user.is_admin:
        return redirect('/home')

    context = {
        'sections':Section.objects.all()
    }
    return render(request, 'dashboard/subject/new_subject.html',context)


def create_subject(request):
    if 'user_id' not in request.session:
        return redirect('/dashboard')
    _user = User.objects.get(id=request.session['user_id'])
    if not _user.is_admin:
        return redirect('/home')

    if request.method=='POST':
        user = User.objects.get(id=request.session['user_id'])
        subject = Subject.objects.create(
            title =request.POST['title'],
            description=request.POST['description'],
            video_url=request.POST['video_url'],
            subject_creator=user,
            section = Section.objects.get(id=request.POST['section'])
    )
    subject.save()
    return redirect('/dashboard/subject')


def edit_subject(request, subject_id):
    if 'user_id' not in request.session:
        return redirect('/dashboard')
    _user = User.objects.get(id=request.session['user_id'])
    if not _user.is_admin:
        return redirect('/home')

    context = {
        'subject':Subject.objects.get(id=subject_id)
    }
    return render(request,'dashboard/subject/edit_subject.html',context)


def update_subject(request, subject_id):
    if 'user_id' not in request.session:
        return redirect('/dashboard')
    _user = User.objects.get(id=request.session['user_id'])
    if not _user.is_admin:
        return redirect('/home')

    if request.method=="POST":
        subject = Subject.objects.get(id=subject_id)
        subject.title=request.POST['title']
        subject.description=request.POST['description']
        subject.video_url=request.POST['video_url']
        subject.save()
    return redirect('/dashboard/subject')

def delete_subject(request, subject_id):
    if 'user_id' not in request.session:
        return redirect('/dashboard')
    _user = User.objects.get(id=request.session['user_id'])
    if not _user.is_admin:
        return redirect('/home')

    subject = Subject.objects.get(id=subject_id)
    subject.delete()
    return redirect('/dashboard/subject')

# End of subjects #
