from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.account import Account
from flask_bcrypt import Bcrypt
import re

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Mons:
    db = 'navdex_schema'

    def __init__(self, data):
        self.id = data['id']
        self.monOne = data['monOne']
        self.monTwo = data['monTwo']
        self.monThree = data['monThree']
        self.monFour = data['monFour']
        self.monFive = data['monFive']
        self.monSix = data['monSix']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.account_id = data['account_id']
        self.account = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM mons JOIN accounts ON mons.account_id=accounts.id;"
        results = connectToMySQL(cls.db).query_db(query)
        mons = []
        for row in results:
            mon = cls(row)
            account_data = {
                'id' : row['accounts.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at': row['accounts.created_at'],
                'updated_at' : row['accounts.updated_at']
            }
            account = Account(account_data)
            mon.account = account
            mons.append(mon)
        return mons

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM mons JOIN accounts ON mons.account_id=accounts.id; WHERE mons.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)

        if len(results) < 1:
            return False

        row = results[0]
        mon = cls(row)
        account_data = {
                'id' : row['accounts.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at': row['accounts.created_at'],
                'updated_at' : row['accounts.updated_at']
            }
        account = Account(account_data)
        mon.account = account

        return mon

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO mons (monOne, monTwo, monThree, monFour, monFive, monSix, account_id) Values (%(monOne)s, %(monTwo)s, %(monThree)s, %(monFour)s, %(monFive)s, %(monSix)s, %(account_id)s);'
        save = connectToMySQL(cls.db).query_db(query, data)
        print(save)
        return save
        

    @classmethod
    def update(cls, data):
        query = 'UPDATE mons SET monOne=%(monOne)s, monTwo=%(monTwo)s, monThree=%(monThree)s, monFour=%(monFour)s, monFive=%(monFive)s, monSix=%(monSix)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM mons WHERE id = %(id)s'
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_mons(mon):
            valid = True

            if len(mon['monOne']) < 3:
                valid = False
                flash("Trainer, I don't recognize the first Pokemon.", 'error')

            if len(mon['monTwo']) < 3:
                valid = False
                flash("Trainer, I don't recognize the second Pokemon.", 'error')
            
            if len(mon['monThree']) < 1:
                valid = False
                flash("Trainer, I don't recognize the third Pokemon.", 'error')

            if len(mon['monFour']) < 3:
                valid = False
                flash("Trainer, I don't recognize the fourth Pokemon.", 'error')

            if len(mon['monFive']) < 3:
                valid = False
                flash("Trainer, I don't recognize the fifth Pokemon.", 'error')

            if len(mon['monSix']) < 3:
                valid = False
                flash("Trainer, I don't recognize the sixth Pokemon.", 'error')

            return valid