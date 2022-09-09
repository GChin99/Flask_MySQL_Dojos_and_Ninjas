# When we have a new table in SQL, we need to crate a new controller file and model file to keep things organized 
# Our controller files have the same imports
from flask_app import app
from flask import Flask, render_template, request, redirect#, session
# We import Dojo beacuase we are going to be using classmethods from our dojo model file
from flask_app.models.dojo import Dojo
# We import Ninja beacuase we are going to be using classmethods from our ninja model file
from flask_app.models.ninja import Ninja


# We are able to use a lot of the same code from our other controller file. 
# We just need to change the variables to fit what we are working with 

@app.route("/ninja")
def make_a_ninja():
    # We already have a classmethod to get all of the dojos that we can use
    # We need all the Dojos to assciate with a ninja instance (need all dojos names for the select tag)
    all_dojos = Dojo.get_all()
    return render_template("create_ninja.html", all_the_dojos = all_dojos)

# ------------------------The C out of CRUD(create)--------------------------------------
@app.route("/create_ninja", methods = ["POST"])
def create_ninja():
    print(request.form)
    # We need to make a data dictionary form our request.form coming from our template
    # The keys in data need to line up exactly with the variables in our query string
    data = {
        # to create a ninja, it takes 4 pieces of info because we need the dojo id that asscoiates with it as well
        "first_name": request.form["first_name"], 
        "last_name": request.form["last_name"],
        "age": request.form["age"],
        "dojo_id": request.form["dojo_id"]
        #left side goes to query in the model file, the right side comes from the form in the HTML file 
    }
    Ninja.create(data) #New class method in the ninja models file
    #Ninja.create(data) becomes the ID that was returned from the classmethod, 
    # return redirect("/")
    return redirect(f"/dojo/{data['dojo_id']}")
    # If we wanted to redirect to the new ninja's info we could have done:
    # new_ninja_id = Ninja.create(data) 
    # return redirect(f"/ninja/{new_ninja_id})

# --------------------The U out of CRUD (update)------------------------------------------------
@app.route("/edit_ninja/<int:id>") #route to a form to edit the ninja
def edit_ninja(id):
    data = {
        "id": id
    }
    # call the classmethod to get one ninja from models folder 
    a_ninja = Ninja.get_one_ninja(data) 
    return render_template("edit_ninja.html", one_ninja = a_ninja)

@app.route("/update_ninja/<int:id>", methods = ["POST"])
def update_ninja(id):
    data = {
        # we need id to target a specific instance like read one and edit
        "id": id,
        # we need to pass the request.form info over like the create route
        "first_name": request.form["first_name"], 
        "last_name": request.form["last_name"],
        "age": request.form["age"],
    }
    # Need get_one_ninja to pull the dojo id to use in the redirect 
    one_ninja = Ninja.get_one_ninja(data)
    Ninja.update_ninja(data) #Need to make a new class method in the models file
    # redirect to the dojo the ninja belongs to. 
    return redirect(f"/dojo/{one_ninja.dojo_id}")


#---------------------THe D out of CRUD (delete)--------------------------------------
@app.route("/delete/<int:id>", methods=["POST"])
def delete_ninja(id):
    data = {
        "id": id
    }
    Ninja.delete(data) #Need to make a new class method in the models file
        # Need get_one_ninja to pull the dojo id to use in the redirect 
    one_ninja = Ninja.get_one_ninja(data)
    return redirect(f"/dojo/{one_ninja.dojo_id}")