from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")



#################################################
# Flask Routes
#################################################
@app.route("/")
def index():

    # Find record of data from the mongo database
    data = mongo.db.data.find_one()

    # Return template and data
    return render_template("index.html", data=data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    data = mongo.db.data

    # Run the scrape function
    mission_mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    data.update({}, mission_mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
