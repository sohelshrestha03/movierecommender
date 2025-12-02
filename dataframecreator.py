import pandas as pd

movie_data={
    "movie_id":[1,2,3,4,5,6,7,8,9,10],

    "movie_title":["Inception","The Dark Knight","Interstellar","Parasite",
        "Avengers: Endgame","The Shawshank Redemption","The Godfather",
        "Forrest Gump","The Matrix","Fight Club"],

    "movie_genre":["Sci-Fi","Action","Sci-Fi","Thriller","Action",
        "Drama","Crime","Drama","Sci-Fi","Drama"],

    "years":[2010,2008,2014,2019,2019,1994,1972,1994,1999,1999],

    "imb_rating":[8.8,9.0,2.6,8.6,8.4,9.3,9.2,1.8,8.7,8.8]
}

df=pd.DataFrame(movie_data)
df.to_csv("movie.csv",index=False)

print("CSV File created successfully")