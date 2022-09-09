# When we have a new table in SQL, we need to crate a new controller file and model file to keep things organized 
from flask_app.config.mysqlconnection import connectToMySQL

# From our HTML form we want to create ninja instances
class Ninja:
    def __init__(self, data):
    # the left had side are the key names we have avaiable for our html file
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.age = data["age"]
        self.dojo_id = data["dojo_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        # ****************Parsing Data into associated Classes **********************
        # If we want one ninjas info we want to be able to pull the one dojo which it comes from
        # data["dojo_id"] would only give us the dojo_id to display.  We want to display the whole dojo instance 
        self.owner = None 



# We are able to use a lot of the same code from our other model file. 
# We just need to change the variables to fit what we are working with 

# ------------------------The C out of CRUD(create)--------------------------------------
    @classmethod
    def create(cls, data): #data is being passed into the class method from the route in the controllers file
        # #the SQL query we want to run, needs to be a string
        # part of the prepared statements.  the %()s is needed, any time user input is used
        # toy_name and color is inserted into the %()s because it is the key in the data dictionry from the controller file (left hand side variable) 
        query = "INSERT INTO ninjas (first_name, last_name, age, dojo_id) VALUES (%(first_name)s, %(last_name)s, %(age)s, %(dojo_id)s);"
        results = connectToMySQL('dojos_and_ninjas').query_db(query, data) #data needs to be added to the query_db because we are passing that information from the data dictionary created in the controllers file
        print(results)
        return results

# -----------------------The R out of CRUD (read one)-------------------------------
    @classmethod
    def get_one_ninja(cls, data): #data is being passed into the class method from the route in the controllers file
        query = "SELECT * FROM ninjas WHERE id = %(id)s"
        results = connectToMySQL('dojos_and_ninjas').query_db(query, data)
        print(results)
        return (cls(results[0]))

# ----------------------------The U out of CRUD(Update)---------------------------------------------
    @classmethod
    def update_ninja(cls, data):
        query = "UPDATE ninjas SET first_name = %(first_name)s, last_name = %(last_name)s, age = %(age)s WHERE id = %(id)s;"
        results = connectToMySQL('dojos_and_ninjas').query_db(query, data) #data needs to be added to the query_db because we are passing that information from the data dictionary created in the controllers file
        print(results)
        return results


# -------------------------The D out of CRUD(delete)---------------------------------------
    @classmethod
    def delete(cls, data): 
        query = "DELETE FROM ninjas WHERE id = %(id)s;"
        results = connectToMySQL('dojos_and_ninjas').query_db(query, data) #data needs to be added to the query_db because we are passing that information from the data dictionary created in the controllers file
        print(results)
        return results