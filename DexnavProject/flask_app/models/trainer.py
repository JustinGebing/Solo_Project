from dataclasses import dataclass
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.scene import Scenes
from flask_bcrypt import Bcrypt
import re

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Trainers:
    db = 'navdex_schema'

    def __init__(self, data):
        self.id = data['id']
        self.trainer = data['trainer']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']

    def __repr__(self) -> str:
        return f"Trainer: {self.trainer}"

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM trainers;"
        results = connectToMySQL(cls.db).query_db(query)
        trainers = []
        for trainer in results:
            trainers.append( cls(trainer) )
        print("trainers", trainers)
        return trainers

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM trainers WHERE trainers.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)

        if len(results) < 1:
            return False
        print(results[0])
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO trainers (trainer) Values (%(trainer)s);'
        save = connectToMySQL(cls.db).query_db(query, data)
        print(save)
        return save
        

    @classmethod
    def update(cls, data):
        query = 'UPDATE trainers SET trainer=%(trainer)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM trainers WHERE id = %(id)s'
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_trainers(trainer):
            valid = True

            if len(trainer['trainer']) < 2:
                valid = False
                flash("He has a better name than that", 'error')

            return valid