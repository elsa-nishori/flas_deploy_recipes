from flask import redirect, render_template, request, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/recipes')
def recipes():
    recipes = Recipe.get_all()
    user_data = {
        'id': session['user_id']
    }
    user = User.get_user_by_id(user_data)
    if recipes:
        return render_template("recipes.html", recipes=recipes, user=user)
    return redirect('/')

@app.route('/recipes/new')
def new_recipe():
    user_data = {
        'user_id': session['user_id']
    }
    return render_template("add_recipe.html", user=user_data)

@app.route('/recipes/add', methods=["POST"])
def add_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    
    Recipe.insert_recipe(request.form)
    return redirect('/recipes')

@app.route('/recipes/<int:id>')
def dashboard(id):
    data = {
        "id": id
    }
    recipe = Recipe.get_recipe(data)
    return render_template("view_recipe.html", recipe=recipe)

@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    data = {
        "id": id
    }
    user_data = {
        'user_id': session['user_id']
    }
    recipe = Recipe.get_recipe(data)
    return render_template("edit_recipe.html", recipe=recipe, user=user_data)

@app.route('/recipes/update', methods=["POST"])
def update():
    Recipe.update_recipe(request.form)
    return redirect('/recipes')
    



