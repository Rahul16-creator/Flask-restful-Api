import sqlite3
from flask import Flask,request
from flask_restful import Resource

class User:
    def __init__(self,_id,username,password):
        self.id=_id
        self.username=username
        self.password=password
    


    @classmethod
    def find_by_name(cls,username):
       connection=sqlite3.connect('database.db')
       cursor=connection.cursor()
       query="SELECT * FROM users WHERE username=?"
       row=cursor.execute(query,(username,))
       result=row.fetchone()
       if result:
           user =cls(*result)
       else:
            user=None
       return user
        

    @classmethod
    def find_by_id(cls,_id):
       connection=sqlite3.connect('database.db')
       cursor=connection.cursor()
       query="SELECT * FROM users WHERE id=?"
       row=cursor.execute(query,(_id,))
       result=row.fetchone()
       if result:
           user =cls(*result)
       else:
            user=None
       return user


class UserRegister(Resource):

    def post(self):

        data=request.get_json()

        connection=sqlite3.connect('database.db')
        cursor=connection.cursor()
        query="SELECT * FROM users WHERE username=?"
        row=cursor.execute(query,(data['username'],))
        result=row.fetchone()
      
        if result:
            return {"error":"username is already exit"},404
            
        query="INSERT INTO users VALUES(Null,?,?)"
        items={"username":data['username'],"password":data['password']}

        cursor.execute(query,(items['username'],items['password']))
        connection.commit()
        connection.close()
        return {"message":"sign-up seccessfully"},200