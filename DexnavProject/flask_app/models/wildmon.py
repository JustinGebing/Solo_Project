from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import wildmon
from flask_bcrypt import Bcrypt
import re

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class WildMons:
    db = 'navdex_schema'

    def __init__(self, data):
        self.id = data['id']
        self.wildMon = data['wildMon']
        self.location = data['location']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM wildmons;"
        results = connectToMySQL(cls.db).query_db(query)
        wildmons = []
        for wildMon in results:
            wildmons.append( cls(wildMon) )
        print("wildmon", wildmons)
        return wildmons

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM wildMons WHERE wildMons.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        print(results[0])

        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO wildMons (wildMon, location) 
        Values (%(wildMon)s, %(location)s)
        ;"""
        save = connectToMySQL(cls.db).query_db(query, data)
        print(save)
        return save
        

    @classmethod
    def update(cls, data):
        query = 'UPDATE wildMons SET wildMon=%(wildMon)s, location=%(location)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM wildMons WHERE id = %(id)s'
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_wildmon(mon):
        valid = True

        if len(mon['wildMon']) < 2:
            valid = False
            flash("Trainer, that's not a pokemon!", 'error')
        
        if len(mon['location']) < 2:
            valid = False
            flash("Trainer, I don't recognize this location!", 'error')

        return valid