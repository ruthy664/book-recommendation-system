### Description

This is a program that will recommend books for you to read based on user preferences. The user will be able to specify books, authors, and genres that they enjoy.

Additionally, the user can specify a desired page length or publication year, and books will only show up that fall within those constraints.

Finally, the user can pick how many books to recommend, with 10 being the default. The system will recommend the specified number of books based on the user's input.

For each recommendation, the system will display the title, cover, description, author, ratings, genres, publication year, and number of pages.

### Data

The data used in this project is from Goodreads.

Goodreads Book Graph Datasets: https://cseweb.ucsd.edu/~jmcauley/datasets/goodreads.html

Since there are a lot of books, the data specifically used for this project is from the Fantasy & Paranormal genre.

Therefore, one of the limitations is that when you are searching for books within a genre such as history, since each book is considered to belong to the Fantasy & Paranormal dataset, the history may just be fantasy history.

### Run Instructions

1. Download the files into a preferred folder.
2. Open a terminal and `cd` to the location of your files.
3. Run: `python -m streamlit run rec_system.py`
