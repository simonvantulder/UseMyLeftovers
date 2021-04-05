from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from . models import *
from . API import *
import math

def index(request):
    return redirect ("/login_page")


def login_page(request):
    return render (request, "login_page.html")


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
        'user': User.objects.get(id = request.session['uuid']),
    }
    return render(request, "view_all.html", context)

def home(request):
    context = {
        "categories": Category.objects.all(),
        'user': User.objects.get(id = request.session['uuid']),
    }
    return render (request, 'kitchen.html', context)


def find_dinner(request):
    request.session["ideas"] = findByIngredientsTasty(request.POST) #store API data in session
    # print(findByIngredientsTasty(request.POST)) #used to troubleshoot navigating through the API dict
    # print(request.session["ideas"][1])

    return redirect ("/make_dinner/results")


def meal_wizard(request):    
    return render (request, "test_form.html")

def meal_wizard_leftovers(request, num):  
    context = {
        "ingredient" : Ingredient.objects.get(id = num)
    }
    return render (request, "test_form.html", context)


def make_dinner_results(request):
    idea = request.session['ideas'] #pull API data 
    # if idea["count"] == 0:
    #     context = {
    #         "no_search_results" : "No matching recipes",
    #         'user': User.objects.get(id = request.session['uuid']),
    #     }
    #     return render(request, "test_form.html", context)
        
    # arr =[]
    # display_arr = []
    # for x in range(len(idea["results"])):
    #     arr.append(x)
    #     display_arr.append(x+1)

    # print(len(idea["results"]))
    # rating_raw = idea['results'][0]['user_ratings']['score'] #number of servings in the recipe 
    # ratings = round(rating_raw * 100)

    context = {
        "idea" : idea,
        # "recipe_list" : idea['results'], #holds all search results 
        # "count" : idea['count'],
        # "counter" : arr,
        'user': User.objects.get(id = request.session['uuid']),

    }
    return render (request, "test_form.html", context)


def make_dinner_num(request, num):
    idea = request.session['ideas'] #pull API data 
    if idea["count"] == 0:
        context = {
            "no_search_results" : "No matching recipes",
            'user': User.objects.get(id = request.session['uuid']),
        }
        return render(request, "test_form.html", context)
        
    arr =[]
    display_arr = []
    for x in range(len(idea["results"])):
        arr.append(x)
        display_arr.append(x+1)

    print(len(idea["results"]))
    # rating_raw = idea['results'][0]['user_ratings']['score'] #number of servings in the recipe 
    # ratings = round(rating_raw * 100)

    context = {
        "idea" : idea,
        "recipe_list" : idea['results'], #holds all search results 
        "count" : idea['count'],
        "counter" : arr,
        'user': User.objects.get(id = request.session['uuid']),

    }
    return render (request, "test_form.html", context)


def add_ingredient_page(request):
    context = {
        'user': User.objects.get(id = request.session['uuid']),
    }

    return render(request, 'add_ingredient.html', context)


def recipe(request, num):
    idea = request.session['ideas'] #pull API data 
    print(idea)
    this_recipe = find_by_id(num)
    print(this_recipe)
    # rating_raw = this_recipe['name'] #recipe rating as decimal
    # rating_raw = this_recipe['user_ratings']['score'] #recipe rating as decimal
    # ratings = round(rating_raw * 100)
    context = {
        'user': User.objects.get(id = request.session['uuid']),
        'recipe': this_recipe,

    }
    return render(request, 'recipe_info.html', context)


def ingredient_add(request):
    num = int(request.POST['category'])
    ingredient = Ingredient.objects.create(
        category = Category.objects.get(id = num),
        name = request.POST['name'],
        quantity = request.POST['quantity'],
        expiration = request.POST['date'],
    )
    return redirect('/view_all/{}'.format(num))


def delete(request, num):
    item = Ingredient.objects.get(id=num)
    number = item.category.id
    item.delete()
    return redirect('/view_all/{}'.format(number))


def logout(request):
    del request.session['uuid']
    
    return redirect("/")

