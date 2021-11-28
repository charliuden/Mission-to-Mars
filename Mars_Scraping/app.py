from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping #the scraping script

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# define the route for the HTML page
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# set up our scraping route. This route will be the "button" of the 
# web application, the one that will scrape updated data when we tell 
# it to from the homepage of our web app. It'll be tied to a button that 
# will run the code when it's clicked.
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302)

# tell flask to run 
if __name__ == "__main__":
   app.run()