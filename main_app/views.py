from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from . models import *
from . API import *
import math

def index(request):
    return redirect ("/login_page")


def login_page(request):
    return render (request, "login_page.html")


def kitchen(request):

    context = {
        "categories" : Category.objects.all(),
        'user': User.objects.get(id = request.session['uuid']),
    }
    return render (request, "kitchen.html", context)


def view_all(request, num):
    this_category = Category.objects.get(id = num)
    context = {
        "category": Category.objects.get(id = num),
        "ingredients" : Category.objects.get(id = num),
    }
    return render(request, "view_all.html", context)

def home(request):
    context = {
        "categories": Category.objects.all(),
        'user': User.objects.get(id = request.session['uuid']),
    }
    return render (request, 'kitchen.html', context)


def dashboard(request):
    context = {
        "name" : User.objects.get(id = request.session['uuid'])
    }
    return render(request, "test_form.html")


def find_dinner(request):
    request.session["ideas"] = findByIngredientsTasty(request.POST) #store API data in session
    # print(findByIngredientsTasty(request.POST)) #used to troubleshoot navigating through the API dict
    # print(request.session["ideas"][1])

    return redirect ("/make_dinner")


def make_dinner(request):
    idea = request.session['ideas'] #pull API data 
    # print(idea['results'])
    print(idea['count'])
    if idea["count"] == 0:
        context = {
            "no_search_results" : "No matching recipes"
        }
        return render(request, "test_form.html", context)
    # rating_raw = idea['results'][0]['user_ratings']['score'] #number of servings in the recipe 
    # ratings = round(rating_raw * 100)

    context = {
        # "ideas" : idea,
        "count" : idea['count'],
        "recipe_list" : idea['results'], #holds all search results 
        "ideas" : idea['results'][9]['sections'][0]['components'], # componenets holds measurements etc other info on each ingredient
        "recipe_num" : idea['results'][9], #holds all key value pairs 
        "instructions" : idea['results'][9]['instructions'], #holds instructions object
        "video" : idea['results'][9]['original_video_url'], #holds instruction video 
        "recipe_picture" : idea['results'][9]['thumbnail_url'], #holds recipe image 
        "servings" : idea['results'][9]['yields'], #number of servings in the recipe 
        "cook_time" : idea['results'][9]['cook_time_minutes'], #total time on the stove and/or in the oven 
        "total_time" : idea['results'][9]['total_time_minutes'], #total time start to finish to make the recipe 
        "nutrition" : idea['results'][9]['nutrition'], #number of servings in the recipe 
        "description" : idea['results'][9]['description'], #descripton of the recipe 
        # "ratings" :  ratings #recipe rating 

    }
    return render (request, "test_form.html", context)


def make_dinner_num(request, num):
    idea = request.session['ideas'] #pull API data 
    if idea["count"] == 0:
        context = {
            "no_search_results" : "No matching recipes"
        }
        return render(request, "test_form.html", context)
    # rating_raw = idea['results'][0]['user_ratings']['score'] #number of servings in the recipe 
    # ratings = round(rating_raw * 100)

    context = {
        "idea" : idea,
        "recipe_list" : idea['results'], #holds all search results 
        "cout" : idea['count'],

        "ideas" : idea['results'][num]['sections'][0]['components'], # componenets holds measurements etc other info on each ingredient
        "recipe_num" : idea['results'][num], #holds all key value pairs 
        "instructions" : idea['results'][num]['instructions'], #holds instructions object
        "video" : idea['results'][num]['original_video_url'], #holds instruction video 
        "recipe_picture" : idea['results'][num]['thumbnail_url'], #holds recipe image 
        "servings" : idea['results'][num]['yields'], #number of servings in the recipe 
        "cook_time" : idea['results'][num]['cook_time_minutes'], #total time on the stove and/or in the oven 
        "total_time" : idea['results'][num]['total_time_minutes'], #total time start to finish to make the recipe 
        "nutrition" : idea['results'][num]['nutrition'], #number of servings in the recipe 
        "description" : idea['results'][num]['description'], #descripton of the recipe 
        # "ratings" :  ratings #recipe rating 

    }
    return render (request, "test_form.html", context)


def user_create(request):
    errors = User.objects.validator(request.POST)
    
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        hash_browns = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name = request.POST["first_name"],
            last_name = request.POST["last_name"],
            email = request.POST["email"],
            password = hash_browns,
            )
        request.session['uuid'] = user.id

    return redirect ("/home")


def login(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        user_list = User.objects.filter(email = request.POST['email'])
        user = user_list[0]
        request.session['uuid'] = user.id 

        return redirect("/home")


def add_ingredient_page(request):

    return render(request, 'add_ingredient.html')


def ingredient_add(request):
    num = int(request.POST['category'])
    ingredient = Ingredient.objects.create(
        category = Category.objects.get(id = num),
        name = request.POST['name'],
        quantity = request.POST['quantity'],
        expiration = request.POST['date'],
    )
    return redirect('/view_all/{}'.format(num))






def logout(request):
    del request.session['uuid']
    
    return redirect("/")

