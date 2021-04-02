import http.client
import requests



def findByIngredientsTasty(post_data):

    url = "https://tasty.p.rapidapi.com/recipes/list"

    ingredient_str = "" #setting up 
    ingredient_list = post_data.getlist('ingredient') #make a list out of the postdata ingredient fields (multiple fields have the same name from jquery appending)
    for ingredient in ingredient_list: #make one long string with commas between each item in ingredient_list
        ingredient_str += ingredient + ','

    querystring = {"from":"0","size":"10","q":f"{post_data['ingred1']}, {post_data['ingred2']},"}
    # querystring = {"from":"0","size":"10","tags":f"under_{post_data['time']}_minutes","q":f"{ingredient_str}"}

    headers = {
        'x-rapidapi-key': "65a692824dmsh49b9f7a37fd2cd8p14f76ajsn4af58bcbc980",
        'x-rapidapi-host': "tasty.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    # print(response.json())
    return(response.json())

def FindTags():
    conn = http.client.HTTPSConnection("tasty.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "65a692824dmsh49b9f7a37fd2cd8p14f76ajsn4af58bcbc980",
        'x-rapidapi-host': "tasty.p.rapidapi.com"
        }

    conn.request("GET", "/tags/list", headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))

def find_by_ingredients(post_data):
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients"

    querystring = {"ingredients":f"{post_data['ingred1']},{post_data['ingred2']},{post_data['ingred3']}","number":"5","ranking":"1","ignorePantry":"true"}

    headers = {
        'x-rapidapi-key': "65a692824dmsh49b9f7a37fd2cd8p14f76ajsn4af58bcbc980",
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

def findRecipe():
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/search"

    querystring = {"query":"burger","cuisine":"thai","diet":"vegetarian","excludeIngredients":"coconut","intolerances":"egg, gluten","number":"10","offset":"0","type":"main course","instructionsRequired":"true"}

    headers = {
        'x-rapidapi-key': "65a692824dmsh49b9f7a37fd2cd8p14f76ajsn4af58bcbc980",
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)
    return(response.text)

