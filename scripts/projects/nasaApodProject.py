import requests
from datetime import date
import datetime
import random


# Description: Gets the data for today's NASA APOD.
# @Parameters: nasa_Key - The NASA API key.
# @Return:     data - The NASA's APOD data for today's date.
def getNasaAPOD(nasa_Key):
    url = "https://api.nasa.gov/planetary/apod?api_key="
    nasa_API_Key = nasa_Key

    today_APOD_URL = url + nasa_API_Key

    data = getNasaData(today_APOD_URL)

    return data

# Description: Gets the data for a random NASA APOD.
# @Parameters: nasa_Key - The NASA API key.
# @Return:     data - The NASA's APOD data for a random date.
def getRandomNasaAPOD(nasa_Key):
    url = "https://api.nasa.gov/planetary/apod?api_key="
    nasa_API_Key = nasa_Key

    random_Date = "&date=" + str(APOD_Random_Date())
    random_APOD_URL = url + nasa_API_Key + random_Date

    data = getNasaData(random_APOD_URL)

    return data

# Description: Gets the data for a specified day NASA APOD.
# @Parameters: nasa_Key - The NASA API key.
#              date - The specified date by the user.
# @Return:     data - The NASA's APOD data for a specified date.
def getCustomNasaAPOD(nasa_Key, date):
    url = "https://api.nasa.gov/planetary/apod?api_key="
    nasa_API_Key = nasa_Key
    date = "&date=" + date

    custom_APOD_URL = url + nasa_API_Key + date

    data = getNasaData(custom_APOD_URL)
    
    return data

# Description: Gets the requested data using the API.
# @Parameters: url_APOD - The url used to request the APOD data.
# @Return:     response - The data response recieved.
def getNasaData(url_APOD):
    response = requests.get(url_APOD)

    return response

# Description: Creates a correctly formatted random date between June 16th 1995 and today, 
# which is the date range of NASA's APOD API.
# @Return:     randDate - The random date created.
def APOD_Random_Date():
    start = datetime.datetime(1995, 6, 16).toordinal()
    end = datetime.date.today().toordinal()

    randDate = randomDate(start, end)

    return randDate

# Description: Returns a random date between 2 specified dates.
# @Parameters: A start and end date.
# @Return: A random date between 2 specified dates.
def randomDate(start, end):
    return date.fromordinal(random.randint(start, end))