from django.shortcuts import render

# Create your views here.

# class Category(models.Model):
#     name = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     category_creator = models.ForeignKey(User,related_name="categories_mader",on_delete=models.CASCADE)


def create_category(request):
    if 'user_id' not in request.session:
        return redirect('/')

    else:
        _user = User.objects.get(id= request.session['user_id'])
        create_cat = Category.objects.create(
            cat_name = request.POST['name'],
            user = _user
        )
        create_cat.save()
        messages.success(request, "Category added successfully!")
        return redirect('/dashboard')

def del_category(request, category_id):

    _category= Category.objects.get(id=category_id)
    _category.delete()

    return redirect('/dashboard')