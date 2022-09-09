# Create a py file named after wahtever we are controlling in a pluralization form 
# All @app.route functions into the controller file
# For this project, we are going with dojos 

from flask_app import app
from flask import Flask, render_template, request, redirect#, session
from flask_app.models.dojo import Dojo #from the models folder, we are importing our Dojo class 


@app.route("/")
def groot():
    return redirect("/dojos")

# ------------------------The R out of CRUD (read all)----------------------------

    # call the query to get all the dojos from the get_all classmethod in the models folder 
@app.route("/dojos")
def dojos():
    all_dojos = Dojo.get_all()
    return render_template("index.html", all_the_dojos = all_dojos)

#---------------------The C out of CRUD (create)---------------------------
@app.route("/create/dojo", methods=["POST"])
def create_dojo():
    # its always a good idea to print the request.from when doing a post route to see the information that is being passed through
    print(request.form)
    # SQL Injections from learn platform 
    # We need to make a data dictionary form out request.form coming from our template
    # The keys in data need to line up exactly with the variables in our query string
    data = {
        "name": request.form["dojo_name"]
        #left side goes to query in the model file, the right side comes from the form in the HTML file 
    }
    Dojo.create(data) #Need to make a new class method in the models file
    return redirect("/dojos")

# ---------------------The R out of CRUD (read one)-----------------------
#This is the app route which will take someone from the main page to the specific Dojo page
@app.route("/dojo/<int:id>") 
def one_dojo(id):
    data = {
        "id": id #this 'id' Key (left side) in data dictionary must be named to match the placeholder in the query. (models folder)
    }
    # ****************Parsing Data into associated Classes**********************
    a_dojo = Dojo.get_one_with_ninjas(data) #new classmethod that JOINS the two SQL tables
    return render_template("one_dojo.html", one_dojo = a_dojo)