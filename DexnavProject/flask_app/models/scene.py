from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.game import Games
from flask import flash
from flask_bcrypt import Bcrypt
import re

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Scenes:
    db = 'navdex_schema'

    def __init__(self, data):
        self.id = data['id']
        self.scene = data['scene']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM scenes;"
        results = connectToMySQL(cls.db).query_db(query)
        scenes = []
        for scene in results:
            scenes.append( Scenes(scene) )
        return scenes

    @classmethod
    def get_one(cls, data):
        query = 'SELECT * from scenes WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        print(results[0])
        return cls(results[0])

    @classmethod
    def get_one_scene(cls, data):
        query = 'SELECT * from scenes WHERE scene = %(scene)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        print(results[0])
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO scenes (scene) Values (%(scene)s);'
        save = connectToMySQL(cls.db).query_db(query, data)
        print(save)
        return save
        

    @classmethod
    def update(cls, data):
        query = 'UPDATE scenes SET scene=%(scene)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM scenes WHERE id = %(id)s'
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_scenes(scene):
        valid = True

        if len(scene['scene']) < 3:
            valid = False
            flash("Trainer, I don't recognize this area!", 'error')

        return valid