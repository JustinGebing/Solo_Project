from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.mon import Mons
from flask_bcrypt import Bcrypt
import re

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Moves:
    db = 'navdex_schema'

    def __init__(self, data):
        self.id = data['id']
        self.moveOne = data['moveOne']
        self.moveTwo = data['moveTwo']
        self.moveThree = data['moveThree']
        self.moveFour = data['moveFour']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.mon_id = ['mon_id']
        self.mons_account_id = ['mons_account_id']
        self.account = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM moves JOIN mons ON moves.mon_id=mons.id;"
        results = connectToMySQL(cls.db).query_db(query)
        moves = []
        for row in results:
            move = cls(row)
            mons_data = {
                'id' : row['mons.id'],
                'monOne' : row['monOne'],
                'monTwo' : row['monTwo'],
                'monThree' : row['monThree'],
                'monFour' : row['monFour'],
                'monFive' : row['monFive'],
                'monSix' : row['monSix'],
                'created_at': row['mons.created_at'],
                'updated_at' : row['mons.updated_at']
            }
            mons = Mons(mons_data)
            move.mons = mons
            moves.append(move)
        return moves

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM moves JOIN mons ON moves.mon_id=accounts.id WHERE moves.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)

        if len(results) < 1:
            return False

        row = results[0]
        move = cls(row)
        mons_data = {
                'id' : row['mons.id'],
                'monOne' : row['monOne'],
                'monTwo' : row['monTwo'],
                'monThree' : row['monThree'],
                'monFour' : row['monFour'],
                'monFive' : row['monFive'],
                'monSix' : row['monSix'],
                'created_at': row['mons.created_at'],
                'updated_at' : row['mons.updated_at']
            }
        mons = Mons(mons_data)
        move.mons = mons

        return move

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO moves (moveOne, moveTwo, moveThree, moveFour, mon_id, mons_account_id) Values (%(moveOne)s, %(moveTwo)s, %(moveThree)s, %(moveFour)s, %(mon_id)s, %(mons_account_id)s);'
        save = connectToMySQL(cls.db).query_db(query, data)
        print(save)
        return save
        

    @classmethod
    def update(cls, data):
        query = 'UPDATE moves SET moveOne=%(moveOne)s, moveTwo=%(moveTwo)s, moveThree=%(moveThree)s, moveFour=%(moveFour)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM scenes WHERE id = %(id)s'
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_scenes(move):
            valid = True

            if len(move['moveOne']) < 1:
                valid = False
                flash("I'm sorry what was this move. Use "--" to signal no move", 'error')
            if len(move['moveTwo']) < 1:
                valid = False
                flash("I'm sorry what was this move. Use "--" to signal no move", 'error')            
            if len(move['moveThree']) < 1:
                valid = False
                flash("I'm sorry what was this move. Use "--" to signal no move", 'error')
            if len(move['moveFour']) < 1:
                valid = False
                flash("I'm sorry what was this move. Use "--" to signal no move", 'error')

            return valid