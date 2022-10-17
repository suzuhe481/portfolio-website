from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/about/")
def about():
    return render_template('about.html', title = "About me")

@app.route("/nasa-picture-of-the-day/", methods=['POST', 'GET']) 
def nasa_api_project():
    return render_template('projects/nasa-picture-of-the-day.html', title = "NASA Astronomy Picture of the Day")