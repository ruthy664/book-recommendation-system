# Book Recommendation System

Data:  https://cseweb.ucsd.edu/~jmcauley/datasets/goodreads.html  

Data Visualization: https://github.com/ruthy664/goodreads-book-data-visualization-and-analysis-dashboard-in-tableau.git  

Intended Audience: Fantasy and Science Fiction readers looking for a new book to read.  

## Description

This is a program that will recommend books for you to read based on user preferences. The user will be able to specify books, authors, and genres that they enjoy.

Additionally, the user can specify a desired page length or publication year, and books will only show up that fall within those constraints.

Finally, the user can pick how many books to recommend, with 10 being the default. The system will recommend the specified number of books based on the user's input.

For each recommendation, the system will display the title, cover, description, author, ratings, genres, publication year, and number of pages.

## Data

The data used in this project is the *Goodreads Book Graph Datasets*. 

Since there are a lot of books, the data specifically used for this project is from the Fantasy & Paranormal genre.

Therefore, one of the limitations is that when you are searching for books within a genre such as history, since each book is considered to belong to the Fantasy & Paranormal dataset, the history may just be fantasy history.

I also created a visualization of the data used in this project, linked above.

<img width="713" height="404" alt="Screenshot 2026-08-31 224416" src="https://github.com/user-attachments/assets/835ec260-ed80-42ef-8332-9ee75c7cce4e" />


## How It Works

Recommendations are given based on popularity, rating, and user preferences. First, each book is given a base score based on its average rating and number of reviews and ratings, and is added to a dataframe with its score. Next, to tailor recommendations to user preferences, any books that don't fit within the required page length or publication year range are removed from the dataframe. Finally, books are given higher scores if they are similar to books the user stated they like (similar book information is provided by the dataset), if they have the same author, or if they fit within the selected genre.

A more detailed overview of the process is included in the notebook.

## Run Instructions

1. Download the files into a preferred folder.
2. Open a terminal and `cd` to the location of your files.
3. Run: `python -m streamlit run rec_system.py`

## Screenshots of the software

<img width="661" height="376" alt="Screenshot 2026-09-01 213327" src="https://github.com/user-attachments/assets/77d31dc1-64f9-4a39-b3bc-d12e1228dc0c" />

<img width="617" height="365" alt="Screenshot 2026-09-01 213342" src="https://github.com/user-attachments/assets/a171cd62-e544-47af-a4eb-74127679224f" />

<img width="590" height="347" alt="Screenshot 2026-09-01 213357" src="https://github.com/user-attachments/assets/eae1c0a1-7482-4f66-a4ca-73703d8a0e18" />
