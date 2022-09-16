from os import stat
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.mon import Mons
from flask_bcrypt import Bcrypt
import re

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Stats:
    db = 'navdex_schema'

    def __init__(self, data):
        self.id = data['id']
        self.level = ['level']
        self.hp = ['hp']
        self.attack = ['attack']
        self.defense = ['defense']
        self.specialA = ['specialA']
        self.specialD = ['specialD']
        self.speed = ['speed']
        self.ability = ['ability']
        self.mon_id = ['mon_id']
        self.mons_account_id = ['mons_account_id']
        self.mon = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM stats JOIN mons ON stats.mon_id=mons.id;"
        results = connectToMySQL(cls.db).query_db(query)
        stats = []
        for row in results:
            stat = cls(row)
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
            stat.mons = mons
            stats.append(stat)
        return stats

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM moves JOIN mons ON moves.mon_id=accounts.id WHERE moves.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)

        if len(results) < 1:
            return False

        row = results[0]
        stat = cls(row)
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
        stat.mons = mons

        return stat

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO stats (level, hp, attack, defense, specialA, specialD, speed, abilit, mon_id, mons_account_id) Values (%(level)s, %(hp)s, %(attack)s, %(defense)s, %(specialA)s, %(specialD)s, %(speed)s, %(ability)s, %(mon_id)s, %(mons_account_id)s);'
        save = connectToMySQL(cls.db).query_db(query, data)
        print(save)
        return save
        

    @classmethod
    def update(cls, data):
        query = 'UPDATE stats SET level=%(level)s, hp=%(hp)s, attack=%(attack)s, defense=%(defense)s, specialA=%(specialA)s, specialD=%(specialD)s, speed=%(speed)s, ability=%(ability)s  WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM stats WHERE id = %(id)s'
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_scenes(stat):
            valid = True

            if len(stat['level']) > 100:
                valid = False
                flash("Pokemon can't go past level 100", 'error')
            if len(stat['level']) < 0:
                valid = False
                flash("Pokemon have to be at least level 1", 'error')
            if len(stat['hp']) < 1:
                valid = False
                flash("hp has to be above 0", 'error')            
            if len(stat['attack']) > 252:
                valid = False
                flash("EV can't be more than 252", 'error')
            if len(stat['attack']) < 0:
                valid = False
                flash("EV can't be negative", 'error')
            if len(stat['defense']) > 252:
                valid = False
                flash("EV can't be more than 252", 'error')
            if len(stat['defense']) < 0:
                valid = False
                flash("EV can't be negative", 'error')
            if len(stat['specialA']) > 252:
                valid = False
                flash("EV can't be more than 252", 'error')
            if len(stat['specialA']) < 0:
                valid = False
                flash("EV can't be negative", 'error')
            if len(stat['specialD']) > 252:
                valid = False
                flash("EV can't be more than 252", 'error')
            if len(stat['specialD']) < 0:
                valid = False
                flash("EV can't be negative", 'error')
            if len(stat['speed']) > 252:
                valid = False
                flash("EV can't be more than 252", 'error')
            if len(stat['speed']) < 0:
                valid = False
                flash("EV can't be negative", 'error')
            if len(stat['ability']) < 0:
                valid = False
                flash("Pokemon has to have an Ability.", 'error')
            return valid