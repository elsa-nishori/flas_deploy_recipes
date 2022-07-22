from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    db_name = "recipes_schema"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.date_cooked = data['date_cooked']
        self.under_30_min = data['under_30_min']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

        self.creator = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes"
        result = connectToMySQL(cls.db_name).query_db(query)
        all_recipes = []
        if not result:
            return False
        for row in result:
            recipe = cls(row)
            all_recipes.append(recipe)
        return all_recipes

    @classmethod
    def insert_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instruction, date_cooked, under_30_min, user_id) VALUES (%(name)s, %(description)s, %(instruction)s, %(date_cooked)s, %(under_30_min)s, %(user_id)s)"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instruction=%(instruction)s, date_cooked=%(date_cooked)s, under_30_min = %(under_30_min)s WHERE id=%(id)s"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_recipe(cls, data):
        query = "SELECT * FROM recipes where id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        all_recipes = []
        if not result:
            return False
        for row in result:
            recipe = cls(row)
            all_recipes.append(recipe)
        return all_recipes[0]

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash("Name should have at least 3 characters")
            is_valid = False

        if len(recipe['description']) < 3:
            flash("Description should have at least 3 characters")
            is_valid = False

        if len(recipe['instruction']) < 3:
            flash("Instructions should have at least 3 characters")
            is_valid = False

        return is_valid