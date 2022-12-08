from fastapi import FastAPI
import pandas as pd
import uvicorn

df = pd.read_csv('all_shows.csv')

app = FastAPI()


@app.get("/")
def read_root(nombre):
    return nombre

@app.get("/get_max_duration")
def get_max_duration(year: int, company: str, category: str):
    print(category)
    if category == "TV Show":
        DF = df[(df['company'] == company) & (df['release_year'] == year)]
        dfMax = DF[DF['seasons'] == DF['seasons'].max()]
        return f'The TV show with the most seasons in {dfMax.iloc[0][8]} for the year {dfMax.iloc[0][4]} is\
{dfMax.iloc[0][2]} with {dfMax.iloc[0][6]} seasons.'

    else:
        DF = df[(df['company']== company) & (df['release_year']== year)]
        dfMax = DF[DF['duration_mins'] == DF['duration_mins'].max()]
        return f'The longest movie in {dfMax.iloc[0][8]} for the year {dfMax.iloc[0][4]} is\
 {dfMax.iloc[0][2]}, it lasts {dfMax.iloc[0][5]} minutes.'


@app.get("/get_count_plataform")
def show_count_two(company: str):
    grouped = df.groupby(['company'])
    grouped = grouped['show_type'].value_counts().to_frame()
    grouped=grouped.rename(columns = {'show_type':'count'})
    grouped = grouped.reset_index()
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
    data = df.listed_in.str.get_dummies(sep=', ').sum()
    data = data.to_frame()
    data = data.rename(columns={0: 'count'}).reset_index()
    data.rename(columns={'index': 'genre'},inplace=True)

    dfMyGenre = data[data['genre'] == genre].reset_index(drop=True)
    myGenreCount =  dfMyGenre.at[0,'count']                         #  genre total

    ver = df.listed_in.str.get_dummies(sep=', ')
    verSeries = ver.pop(genre)
    mySeries = df['company']
    verComp = pd.concat([verSeries, mySeries], axis=1)
    verComp = verComp[verComp[genre] == 1]                        # Filter
    vCGroup = verComp.groupby('company')
    ff = vCGroup[genre].value_counts().to_frame()
    ff = ff.rename(columns={genre:'count'}).reset_index()
    ff = ff[ff['count'] == ff['count'].max()]

    return f'Existen {myGenreCount} registros del genero {genre}. La plataforma con mayor oferta de este genero es \
{ff.at[0,"company"]} con {ff.at[0,"count"]} series y peliculas.'


@app.get("/actor")
def max_performer(company: str, year: int):    # Cuando lo lleves raw Py tenés que tipar los parámetros company: str  year: int
    if company == 'Hulu':
        return 'There are no records for this category in Hulu'
    else:
        DF = df[(df['company']== company) & (df['release_year'] == year)]
        DF = DF.cast.str.get_dummies(sep=', ').sum()
        DF = DF.to_frame().reset_index().rename(columns={"index": "genre", 0:'total'})
        DF = DF[DF.total == DF.total.max()]

        return f'The performer with the most apparitions in {company} in {year} is {DF.iloc[0][0]}, with a total of\
 {DF.iloc[0][1]} movies and tv shows.'

# The statement below is just another way of refreshing the server, instead of using the command 'uvicorn -- reload'.
# In the terminal we have to start our server by calling this script with the following command 'main.py' or
# 'python main.py'.
if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0')
