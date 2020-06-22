from flask import Flask,request
from flask_restful import Api,Resource
from flask_jwt import JWT,jwt_required
import sqlite3

from usertable import authenticate,identity
from user import UserRegister
app=Flask(__name__)
api=Api(app)
app.secret_key="RK"
jwt=JWT(app,authenticate,identity)

class Items(Resource):

    @jwt_required()
    def get(self,name):
        connection=sqlite3.connect("database.db")
        cursor=connection.cursor()

        query="SELECT * FROM items WHERE name=?"
        result=cursor.execute(query,(name,))
        row=result.fetchone()
        connection.close()
        if row:
            return {"name":row[0],"price":row[1]},201
        return {"error":"Item not found"},404


    @jwt_required()
    def post(self,name):
        request_data=request.get_json()
        connection=sqlite3.connect("database.db")
        cursor=connection.cursor()
        items={
            "name":name,
            "price":request_data['price']
        }
        query="INSERT INTO items VALUES(?,?)"
        cursor.execute(query,(items['name'],items['price']))
        connection.commit()
        connection.close()
        return {"success":"Items stored"}



    @jwt_required()
    def delete(self,name):
        
        connection=sqlite3.connect("database.db")
        cursor=connection.cursor()

        query="DELETE FROM items WHERE name=?"
        cursor.execute(query,(name,))
        connection.commit()
        connection.close()
        return "item deleted successfull"


    @jwt_required()
    def put(self,name):
        data=request.get_json()
        connection=sqlite3.connect('database.db')
        cursor=connection.cursor()
        items={"name":name,"price":data['price']}
        query="SELECT * FROM items WHERE name=?"
        result=cursor.execute(query,(name,))
        row=result.fetchone()
        if row:
            query="UPDATE items SET price=? WHERE name=?"
            cursor.execute(query,(items['price'],items['name'],))
            connection.commit()
            connection.close()
        else:
            
            query="INSERT INTO items VALUES(?,?)"
            cursor.execute(query,(items['name'],items['price']))
            connection.commit()
            connection.close()
        return items


class AllItems(Resource):
    def get(self):
        items=[]
        connetion=sqlite3.connect('database.db')
        curor=connetion.cursor()

        query="SELECT * FROM items"
        result=curor.execute(query)

        for name in result:
           items.append({"name":name[0],"price":name[1]})
        return items



api.add_resource(Items,'/item/<string:name>')
api.add_resource(AllItems,'/items')
api.add_resource(UserRegister,'/register')



app.run(debug=True)