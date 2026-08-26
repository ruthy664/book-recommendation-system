# recomend_books

import pandas as pd
import ast

# Get the dataframes 
authors_grouped_df = pd.read_csv('data/authors_grouped.csv')
authors_grouped_df['book_id'] = authors_grouped_df['book_id'].apply(ast.literal_eval)

genres_grouped_df = pd.read_csv('data/genres_grouped.csv')
genres_grouped_df['book_id'] = genres_grouped_df['book_id'].apply(ast.literal_eval)

recommendations_df = pd.read_csv('data/recommendations.csv')
recommendations_df['similar_books'] = recommendations_df['similar_books'].apply(ast.literal_eval)

books_df = pd.read_csv('data/books_reduced.csv')
authors_to_books_df = pd.read_csv('data/authors_to_books_reduced.csv')
authors_df = pd.read_csv('data/authors_reduced.csv')
genres_list_df = pd.read_csv('data/genres_list.csv')
genres_list_df['genres'] = genres_list_df['genres'].apply(ast.literal_eval)


# ----------- Funtions --------------

def update_authors(df, authors, score):
    for author in authors:
        books = authors_grouped_df['book_id'][authors_grouped_df['author_id'] == author].values[0]
        df.loc[df['book_id'].isin(books), 'recommendation_score'] += score
    return df

def update_genres(df, genres, score):
    for genre in genres:
        books = genres_grouped_df['book_id'][genres_grouped_df['genres'] == genre].values[0]
        df.loc[df['book_id'].isin(books), 'recommendation_score'] += score
    return df

def update_similar_books(df, books, score):
    df = df[~df['book_id'].isin(books)]
    
    for book_id in books:
        similar_books = recommendations_df.loc[
            recommendations_df['book_id'] == book_id, 'similar_books'
        ].values[0]
        df.loc[df['book_id'].isin(similar_books), 'recommendation_score'] += score
    
    return df

def update_pages(df, p1, p2):
    df = df[(df['num_pages']>=p1) & (df['num_pages']<=p2)]
    return df

def update_years(df, y1, y2):
    df = df[(df['publication_year']>=y1) & (df['publication_year']<=y2)]
    return df

def get_recomendation_score(authors=[], genres=[], books=[], pages=[], years=[]):
    personalized_recommendations_df = recommendations_df.copy()
    
    if authors:
        n = len(authors)
        score = 1/(2*n)
        personalized_recommendations_df = update_authors(personalized_recommendations_df, authors, score)
    
    if genres:
        n = len(genres)
        score = 1/n
        personalized_recommendations_df = update_genres(personalized_recommendations_df, genres, score)

    if books:
        n = len(books)
        score = 1/n
        personalized_recommendations_df = update_similar_books(personalized_recommendations_df, books, score)

    if len(pages)==2:
        p1 = min(pages)
        p2 = max(pages)
        personalized_recommendations_df = update_pages(personalized_recommendations_df, p1, p2)

    if len(years)==2:
        y1 = min(years)
        y2 = max(years)
        personalized_recommendations_df = update_years(personalized_recommendations_df, y1, y2)

    return personalized_recommendations_df

def recommend_books(authors=[], genres=[], books=[], pages=[], years=[], x=10):
    # Get the personalized_recommendations_df
    personalized_recommendations_df = get_recomendation_score(authors=authors, genres=genres, books=books, pages=pages, years=years)
    
    # Get the top scores in the df
    top_df = personalized_recommendations_df.nlargest(x, 'recommendation_score')[['book_id', 'recommendation_score']].reset_index(drop=True)
    
    # Add title and ratings to df
    top_df = top_df.merge(books_df[['book_id', 'title', 'average_rating', 'ratings_count']], on='book_id', how='left')
    
    # add authors to df
    top_df["authors"] = None
    
    for i in range(len(top_df)):
        entry = ""
        book_id = top_df.loc[i, 'book_id']
        auth = authors_to_books_df[authors_to_books_df['book_id']==book_id].reset_index(drop=True)
        rows = auth.shape[0]
        for row in range(rows):
            author_id = auth.loc[row, "author_id"]
            author_name = authors_df.loc[
                authors_df['author_id']==author_id,
                "name"
            ].values[0]
            role = auth.loc[row, "role"]

            entry += author_name
            if pd.notna(role):
                entry += f" ({role})"
            
            if row != (rows-1):
                entry += ", "
        top_df.loc[i, "authors"] = entry

    # Add publisher, year written, number of pages, url, and image url
    top_df = top_df.merge(books_df[['book_id', 'publisher', 'publication_year', 'num_pages', 'url', 'image_url']], on='book_id', how='left')

    # Add genres
    top_df = top_df.merge(genres_list_df[['book_id', 'genres']], on='book_id', how='left')

    # Add description
    top_df = top_df.merge(books_df[['book_id', 'description']], on='book_id', how='left')

    return top_df