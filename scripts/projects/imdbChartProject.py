import imdb
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import re       # Used to create regex.

# Used to save and encode heatmap as an image to send to user.
import io
import base64


# Description: Creates the heatmap by executing a sequence of other functions.
# @Parameters: showID - The ID of the show being used.
# @Return:     heatmap - The heatmap created from the show.
def createChart(showID, chartColor):
    series, ratingsArr, lowestRated = createRatingsArray(showID)

    # Creates the heatmap using above variables.
    heatmap = createRatingHeatmap(ratingsArr, series, lowestRated, chartColor)

    return heatmap

# Description: Checks if a submitted link is a valid show series from imdb.
# @Parameters: link - The link submitted.
# @Return:     A boolean.
def validateIMDBLink(link):
    # Regex imdbSite... to check if string contains "imdb.com".
    # Regex imdbShow... to check if string contains "title/tt" followed by any number of digits.
    imdbSiteCheckPattern = re.compile("imdb.com")
    imdbShowCheckPattern = re.compile("title/tt[\\d]+/")

    if imdbSiteCheckPattern.search(link) and imdbShowCheckPattern.search(link) and imdbSiteCheckShoworMovie(link):
        # print("Website is imdb and valid show.")

        return True
    else:
        # print("Website is NOT imdb or valid show.")

        return False

# Description: Checks if a link corresponds to a tv series.
# @Parameters: link - The link submitted.
# @Return: A boolean.
def imdbSiteCheckShoworMovie(link):
    showId = extractID(link)
    ia = imdb.IMDb()
    series = ia.get_movie(showId)

    if series['kind'] == 'tv series':
        print(series['kind'])
        print("It's a series")
        return True
    else:
        print(series['kind'])
        print("Not a series")
        return False

# Description: Splits the validated link to extract the show's ID.
# @Parameters: link - The link submitted.
# @Return:     showID - the show's ID.
def extractID(link):
    # Stores the link as an array separated by the '/'.
    linkArr = re.split("/", link)
    # print(x)

    # Gets the array index after "title".
    showID_index_at = linkArr.index("title") + 1
    print(showID_index_at)

    # Gets the array element that contains the show's ID.
    unchecked_showID = linkArr[showID_index_at]
    print(unchecked_showID)

    # Removes the first 2 characters of the array, which isn't needed.
    # tt###### => ######
    showID = unchecked_showID[2:]

    return showID



# Description: Creates an instance of the imdB class and imports an show inputted by a user. 
#              Creates an array of the show's ratings.
# @Parameters: inputShowId - ID of show selected by user.
# @Return:     seriesName - Name of the series.
#              ratingArr - A 2D array of the show's ratings.
def createRatingsArray(inputShowId):
    
    # Variables storing the lowest rated episode. Used for vmin in heatmap.
    # Starts at 10, then goes down.
    lowestRated = 10

    # Creates access object of the IMDb class.
    ia = imdb.IMDb()
    
    # Initializing the main array.
    ratingArr = []

    # Pick show to import.
    series = ia.get_movie(inputShowId)

    # print('start')
    # print(ia)
    # print(series['kind'])
    # print('end')

    try:
        # Retrieves the episodes from the specifies show.
        ia.update(series, 'episodes')
    except:
        print("error")
    
    # Goes through each episode to create a 2D array of show's ratings.
    for season_nr in sorted(series['episodes']):
        # Does not include seasons listed as "Unknown" on IMDb. 
        if season_nr <= 0:
            continue

        # Initializing the season array.
        season = []

        # Goes through every season.
        for episode_nr in sorted(series['episodes'][season_nr]):
            episode = series['episodes'][season_nr][episode_nr]

            # Stores a single episode's rating to 2 decimal points if it exists.
            if episode.get('rating')==None:
                continue
            rating = (round(episode.get('rating'), 2))

            if rating < lowestRated:
                lowestRated = rating

            # Appends the episode's rating to the season array.
            season.append(rating)

        # Appends a single season to the show's array.
        ratingArr.append(season)

    # Finding the row with the maximum length.
    # Then pads each row with zeros to have the same length as the longest row.
    maxLen = 0
    for row in ratingArr:
        if maxLen < len(row):
            maxLen = len(row)
    for i in range(0, len(ratingArr)):
        newRow = np.pad(ratingArr[i], ((0, (maxLen-len(ratingArr[i])))), 'constant' )
        ratingArr[i] = newRow

    # Converts the array into a numpy array.
    ratingArr = np.array(ratingArr)

    # Transpose is done to get seasons on x-axis and episodes on y-axis.
    ratingArr = ratingArr.T
    
    return series, ratingArr, lowestRated



# Description: Creates a heatmap of the ratings using a 2D array.
# @Parameters: ratingsArray - The 2D array of the show's ratings.
# @Return:     imgB64String - An encoded png image of a heatmap of a show's ratings.
def createRatingHeatmap(ratingsArray, series, lowestRated, chartColor):
    
    # Creates the intervals for the x and y axis.
    seasonsX = list(range(1, len(ratingsArray[0])+1))
    episodesY = list(range(1, len(ratingsArray)+1))

    # Creates a figure.
    fig, ax = plt.subplots(figsize=(len(ratingsArray[0])*2, len(ratingsArray)))
    
    # Moves the ticks of the x axis to the top of the heatmap.
    ax.xaxis.tick_top()

    # Creats a mask that hides 0s on the heatmap. IMDb doesn't allow for 0 ratings.
    hideZeroMask = (ratingsArray == 0)

    # Inputs the data of the show's ratings into an seaborn heatmap.
    sns.heatmap(ratingsArray,vmin=lowestRated,vmax=10, annot=ratingsArray, linewidth=0.3, cmap=chartColor,
                mask=hideZeroMask, xticklabels=seasonsX, yticklabels=episodesY)

    # Labels the title, x-axis, and y-axis.
    plt.title(series)
    plt.xlabel("Seasons")
    plt.ylabel("Episodes")

    # Rotates the y-axis labels to be at a readable orientation.
    plt.yticks(rotation=0)

    # Moves the title of the x-axix to the top.
    ax.xaxis.set_label_position('top')

    fig.tight_layout()
    # plt.show()

    # Source: https://gitlab.com/snippets/1924163
    # Source gotten from Source 2: https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
    # Saves the heatmap as bytes.
    img = io.BytesIO()
    plt.savefig(img, format='png')
    
    # Encodes the image to a base64 string.
    imgB64String = "data:image/png;base64,"
    imgB64String += base64.b64encode(img.getvalue()).decode('utf8')

    return imgB64String
