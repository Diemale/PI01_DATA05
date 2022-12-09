from fastapi import FastAPI
import pandas as pd
import uvicorn

# Import data
df = pd.read_csv('all_shows.csv')

# create the app
app = FastAPI()

### Create the functions to make the requests

## Test function
@app.get("/")
def read_root(nombre):
    return nombre

## Main functions
# These functions use type hints to restrict the data type used in the queries (i.e. year: int means the input data
# type must be an integer. Otherwise, the user will receive an instant error message).

@app.get("/get_max_duration")
def get_max_duration(year: int, company: str, category: str):
    if category == "TV Show":                                               # if the input value is "Tv Show"
        DF = df[(df['company'] == company) & (df['release_year'] == year)]  # filter by company and year
        dfMax = DF[DF['seasons'] == DF['seasons'].max()]            # create a new DF with only 'max seasons' row
        # create a return string with the data we need from the last DataFrame
        return f'The TV show with the most seasons in {dfMax.iloc[0][8]} for the year {dfMax.iloc[0][4]} is \
{dfMax.iloc[0][2]} with {dfMax.iloc[0][6]} seasons.'

    else:                                                              # Valid input "Movie"
        DF = df[(df['company']== company) & (df['release_year']== year)]  # filter by company and year
        dfMax = DF[DF['duration_mins'] == DF['duration_mins'].max()]      # create a new DF with only 'max seasons' row
         # create a return string with the data we need from the last DataFrame
        return f'The longest movie in {dfMax.iloc[0][8]} for the year {dfMax.iloc[0][4]} is\
 {dfMax.iloc[0][2]}, it lasts {dfMax.iloc[0][5]} minutes.'


@app.get("/get_count_plataform")
def show_count_two(company: str):
    grouped = df.groupby(['company'])                            # Group data by 'company' column
    grouped = grouped['show_type'].value_counts().to_frame()   # count grouped values, and convert the resulting Series to a DataFrame
    grouped = grouped.rename(columns={'show_type': 'count'})   # rename column to allow an index reset
    grouped = grouped.reset_index()                            # reset the index to work neatly
    # Get a return string showing the needed data for every possible company
    if company == "Amazon Prime":
        return f'{grouped.iloc[0][0]} has listed {grouped.iloc[0][2]} movies and {grouped.iloc[1][2]} TV Shows.'
    elif company == "Disney":
        return f'{grouped.iloc[2][0]} has listed {grouped.iloc[2][2]} movies and {grouped.iloc[3][2]} TV Shows.'
    elif company == "Hulu":
        return f'{grouped.iloc[4][0]} has listed {grouped.iloc[5][2]} movies and {grouped.iloc[4][2]} TV Shows.'
    else:
        return f'{grouped.iloc[6][0]} has listed {grouped.iloc[6][2]} movies and {grouped.iloc[7][2]} TV Shows.'


@app.get("/listedin")
def get_genre_qt(genre: str):
    # get the sum of every single value from a column with multiple-value cells
    data = df.listed_in.str.get_dummies(sep=', ').sum()
    data = data.to_frame()                                  # convert the Series to a DataFrame
    data = data.rename(columns={0: 'count'}).reset_index()  # rename column to allow an index reset
    data.rename(columns={'index': 'genre'}, inplace=True)   # same as above

    dfMyGenre = data[data['genre'] == genre].reset_index(drop=True)  # filter DataFrame by the input genre
    myGenreCount =  dfMyGenre.at[0,'count']                         # save genre total (int)

    # Convert a column with multiple-value cells to a Data-Frame with one column for
    # every unique value(pretty similar to one-hot-encoding)
    ver = df.listed_in.str.get_dummies(sep=', ')

    verSeries = ver.pop(genre)       # create a Series by popping the column with an equal name to the input parameter
    mySeries = df['company']         # create a company Series from the original DataFrame
    verComp = pd.concat([verSeries, mySeries], axis=1)      # concatenate both Series
    verComp = verComp[verComp[genre] == 1]                   # Filter the resulting DataFrame by the input genre
    vCGroup = verComp.groupby('company')                   # Group by company
    ff = vCGroup[genre].value_counts().to_frame()    # count grouped values, convert the resulting Series to a DataFrame
    ff = ff.rename(columns={genre:'count'}).reset_index()   # reset the index to work neatly
    ff = ff[ff['count'] == ff['count'].max()]          # filter the DataFrame to get a new one-row DF with the max-count

    # Return a string with the requested data
    return f'Existen {myGenreCount} registros del genero {genre}. La plataforma con mayor oferta de este genero es \
{ff.at[0,"company"]} con {ff.at[0,"count"]} series y peliculas.'


@app.get("/actor")
def max_performer(company: str, year: int):
    if company == 'Hulu':
        return 'There are not records for this category in Hulu'  # There aren't actor values in Hulu's DataSet
    else:                                                                   # For the other companies
        DF = df[(df['company'] == company) & (df['release_year'] == year)]  # filter by company and year
        # get the sum of every single value from a column with multiple-value cells
        DF = DF.cast.str.get_dummies(sep=', ').sum()
        DF = DF.to_frame().reset_index().rename(columns={"index": "genre", 0:'total'})  # rename columns
        DF = DF[DF.total == DF.total.max()]           # filter the DataFrame to get a new one-row DF with the max-count

        # Return a string with the requested data
        return f'The performer with the most apparitions in {company} in {year} is {DF.iloc[0][0]}, with a total of\
 {DF.iloc[0][1]} movies and tv shows.'

# The statement below is just another way of refreshing the server, instead of using the command 'uvicorn -- reload'.
# In the terminal we have to start our server by calling this script with the following command 'main.py' or
# 'python main.py'.
if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0')
