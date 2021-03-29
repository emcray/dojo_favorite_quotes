from django.shortcuts import render, redirect
from login_app.models import User, UserManager
from .models import Quote, QuoteManager, Author, AuthorManager
from django.db.models import Count
from django.contrib import messages

def home(request):
    context = {
        'quote': Quote.objects.all(),
        'current_user': User.objects.get(id = request.session['user_id'])
    }
    return render(request, 'home.html', context)

def create_quote(request):
    author_error = Author.objects.author_validate(request.POST)
    if len(author_error) > 0:
        for key, value in author_error.items():
            messages.error(request, value)

    quote_error = Quote.objects.quote_validate(request.POST)
    if len(quote_error) > 0:
        for key, value in quote_error.items():
            messages.error(request, value)
    
    if len(messages.get_messages(request)) > 0:
        return redirect ('/quotes')
    
    else:
        author = Author.objects.create(name = request.POST['author_name'])
        user = User.objects.get(id=request.session['user_id'])
        Quote.objects.create(
            content = request.POST['quote'], 
            author = author, 
            posted_by = user
            )
    print(request.POST)
    return redirect('/quotes')

def user_quotes(request, user_id):
    context = {
        'poster': User.objects.get(id=user_id),
        'quotes': Quote.objects.all()
    }
    return render(request, 'quote.html', context)

def profile(request):
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'profile.html', context)

def update_user(request, user_id):
    user_error = User.objects.update_validate(request.POST)
    if len(user_error) > 0:
        for key, value in user_error.items():
            messages.error(request, value)
        return redirect('/quotes/profile')

    else:
        edit_user = User.objects.get(id=request.session['user_id'])
        edit_user.first_name = request.POST['first_name']
        edit_user.last_name = request.POST['last_name']
        edit_user.email = request.POST['email']
        edit_user.save()
        print(request.POST)
        return redirect('/quotes/profile')

def like(request, quote_id): ##come back to. method not correct
    liked_quote = Quote.objects.get(id=quote_id)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_quote.liked_by.add(user_liking)
    return redirect('/quotes')

def delete(request, quote_id):
    delete = Quote.objects.get(id=quote_id)
    delete.delete()
    return redirect('/quotes')

def logout(request):
    request.session.flush()
    return redirect('/')
