#In the models folder, we need to create a folder and name in the singlar verson of the file in the controllers folder
#In this case, it would be called dojo

# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# We need to import the ninja class from our models
from flask_app.models import ninja

class Dojo:
    def __init__(self, data):
        # the left had side are the key names we have avaiable for our html file
        self.id = data["id"]
        self.dojo_name = data["name"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        # ****************Parsing Data into associated Classes *********************
        # We are creating an empty list so we can append the ninjas into
        self.ninjas = []

        # -------------------The R out of CRUD (read all)-----------------------------
# Now we use class methods to query our database.
#  We use class method to get all the instances from the database 
    @classmethod
    def get_all(cls):
        # we need to use a string of the SQL query we want to run 
        query = "SELECT * FROM dojos;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        # We are asking the function to connect to our database and run the query that we stated above
        results = connectToMySQL('dojos_and_ninjas').query_db(query)
        # Best practice to print results to see if it pulled the correct infomration from the database.  If there was any issues, it would print False 
        print(results)
        # Create an empty list to append our instances of dojos
        all_dojos = []
        # Iterate over the db results and create instances of dojos with cls.
        for one_dojo in results:
            all_dojos.append(cls(one_dojo))
        return all_dojos #return the list of appended instances of dojos

# ------------------------The C out of CRUD(create)--------------------------------------
#   We use class method to create new dojo instances in our database 
    @classmethod
    def create(cls, data): #data is being passed into the class method from the route in the controllers file
        # part of the prepared statements.  the %()s is needed, any time user input is used
        query = "INSERT INTO dojos (name) VALUES (%(name)s);"
        results = connectToMySQL('dojos_and_ninjas').query_db(query, data) #data needs to be added to the query_db because we are passing that information from the data dictionary created in the controllers file
        print(results)
        return results


# ****************Parsing Data into associated Classes**********************
# -----------------------New Read class method to JOIN dojos and ninjas (read one)-------------------------------
    @classmethod
    def get_one_with_ninjas(cls, data): #data is being passed into the class method from the route in the controllers file
        #The SQL query is differnt from the one above. We want to JOIN the dojos and ninjas tables 
        query = "SELECT * FROM dojos JOIN ninjas ON dojos.id = ninjas.dojo_id WHERE dojos.id = %(id)s;"
        results = connectToMySQL('dojos_and_ninjas').query_db(query, data) #data needs to be added to the query_db because we are passing that information from the data dictionary created in the controllers file
        print(results)
        # If an dojo has more than 1 ninja, the the query repeats the dojo info everytime it displays a ninja. (look at print statement from this class)
        # We only want to display the dojo info once, but shows all the toys it has.
        # we are creating an dojo instance from the first dictionary entry that we get back
        one_dojo = cls(results[0])
        # We are going to loop through all the indexes in the list of dictionaries to pull out all the ninja information
        # We will appened the ninja instances into the empty list that we made in the constructor 
        for one_ninja in results:
            data = {
                # Left side keys are from the Ninja class (models file) = ride side keys are the results from the database query (print statement)
                "id" : one_ninja["ninjas.id"], #we use "ninjas.id" becuase "id" is already being used by the dojo self.id = data["id"]
                "first_name" :one_ninja["first_name"],
                "last_name" : one_ninja["last_name"],
                "age": one_ninja["age"],
                "dojo_id": one_ninja["dojo_id"],
                "created_at": one_ninja["ninjas.created_at"],#we use "ninjas.created_at" becuase "created_at" is already being used by the dojo self.created_at = data["created_at"]
                "updated_at": one_ninja["ninjas.updated_at"]#we use "ninjas.updated_at" becuase "updated_at" is already being used by the dojo self.updated_at = data["updated_at"]
            }
            ninja_obj = ninja.Ninja(data) #we are creating a ninja instance by bring the Ninja class over to the dojo
            one_dojo.ninjas.append(ninja_obj)
            # We are saying one_dojo has an attribue called dojo and we are appending the ninja instance we just crated to the empty list ninjas 
        return one_dojo