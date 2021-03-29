from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, UserManager
import bcrypt

def home(request):
    return render(request, 'login.html')

def register(request):
    errors = User.objects.reg_validate(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
            print(request.POST)
        return redirect('/')
    
    else:
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        )

        request.session['user_id'] = new_user.id
        request.session['greeting'] = new_user.first_name #this will be placed on profile page under books app
        return redirect('/quotes') #will need to replace with books profile redirect

def login(request):
    errors = User.objects.login_validate(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ('/')

    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
        return redirect('/quotes') #will need to replace with books once page is built

#def success(request):
    #return render(request, 'success.html')
