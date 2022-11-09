from flask import Flask, render_template, request
import config

import scripts.projects.nasaApodProject as nasaModule
import scripts.projects.imdbChartProject as imdbModule

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/all-projects/")
def all_projects():
    return render_template('all-projects.html', title = "All Projects")


@app.route("/about/")
def about():
    return render_template('about.html', title = "About me")


@app.route("/nasa-picture-of-the-day/", methods=['POST', 'GET']) 
def nasa_api_project():
    # Recieving data from the form.
    if request.method == "POST" and "nasa-form" in request.form:
        formData = request.form.to_dict()

        # Retrieving today's Nasa's Astronomy Picture of the Day.
        if formData.get("nasa-form") == "getToday":
            print("Getting today's NASA image")

            returned_APOD_Data = nasaModule.getNasaAPOD(config.nasa_API_key)        # Gets the response object.
            returned_APOD_JSON = returned_APOD_Data.json()                          # Takes a response and returns a promise.

        # Retrieving a random Nasa's Astronomy Picture of the Day.
        elif formData.get("nasa-form") == "getRandom":
            print("Getting a random Nasa image")

            returned_APOD_Data = nasaModule.getRandomNasaAPOD(config.nasa_API_key)  # Gets the response object.
            returned_APOD_JSON = returned_APOD_Data.json()                          # Takes a response and returns a promise.
        # Retrieving a user specified Nasa's Astronomy Picture of the Day.
        elif formData.get("nasa-form") == "getCustom":
            print("Getting a custom dated NASA image")
            pickedDate = formData.get("pickedDate")

            returned_APOD_Data = nasaModule.getCustomNasaAPOD(config.nasa_API_key, pickedDate)      # Gets the response object.
            returned_APOD_JSON = returned_APOD_Data.json()                                          # Takes a response and returns a promise.

    # Renders default NASA project page.
    else:
        return render_template('projects/nasa-picture-of-the-day.html', title = "NASA Astronomy Picture of the Day")

    # Renders NASA project page with data.
    return render_template('projects/nasa-picture-of-the-day.html', title = "NASA Astronomy Picture of the Day", nasa_Data=returned_APOD_JSON)


@app.route("/imdb-ratings-chart/", methods=['POST', 'GET'])
def imdb_project():
    if request.method == "POST":
        # imdbLink = request.form.get("imdbLink")
        formData = request.form.to_dict()

        # print("imdb link is below")
        # print(imdbLink)
        # console.logger(imdbLink)
        app.logger.info("form data is:")
        app.logger.info(formData)

        app.logger.info("link is:")
        app.logger.info(formData.get("imdbLink"))
        imdbLink = formData.get("imdbLink")

        app.logger.info("color is:")
        app.logger.info(formData.get("chart-color"))



        # Creates a heatmap if the link is a valid show.
        if imdbModule.validateIMDBLink(imdbLink):
            showID = imdbModule.extractID(imdbLink)
            chartColor = formData.get("chart-color")

            showRatingsChart = imdbModule.createChart(showID, chartColor)

            return render_template('projects/imdb-ratings-chart.html', title="IMDB Ratings Chart", imdbLink=imdbLink, showRatingsChart=showRatingsChart)
        # Returns an error if show is not valid.
        else:
            return render_template('projects/imdb-ratings-chart.html', title="IMDB Ratings Chart", error="Link must be from a series with multiple episodes.")
    else:
        return render_template('projects/imdb-ratings-chart.html', title="IMDB Ratings Chart")
