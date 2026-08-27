# Run instructions:
# cd 'C:\[your_file_path]'
# python -m streamlit run rec_system.py


import pandas as pd
import streamlit as st
import recomend_books

@st.cache_data
def load_authors():
    return pd.read_csv('data/authors_reduced.csv')

@st.cache_data
def load_genres():
    return pd.read_csv('data/genres_grouped.csv')

@st.cache_data
def load_books():
    return pd.read_csv('data/books_reduced_limited.csv')

authors_df = load_authors()
genres_df = load_genres()
books_df = load_books()


def render_search_and_add(label, df, search_col, id_col, session_key, max_results=10):
    """Compact search box + add-to-list UI. Stores {'id': ..., 'label': ...} dicts."""
    if session_key not in st.session_state:
        st.session_state[session_key] = []

    query = st.text_input(f"Search {label}", key=f"search_{session_key}")

    if query:
        matches = df[df[search_col].str.contains(query, case=False, na=False)].head(max_results)
    else:
        matches = df.iloc[0:0]

    selected_ids = {item["id"] for item in st.session_state[session_key]}

    for idx, row in matches.iterrows():
        c1, c2 = st.columns([5, 1])
        c1.caption(row[search_col])
        already_added = row[id_col] in selected_ids
        if c2.button("Add" if not already_added else "Added", key=f"{session_key}_add_{idx}", disabled=already_added):
            st.session_state[session_key].append({"id": row[id_col], "label": row[search_col]})
            st.rerun()

    if st.session_state[session_key]:
        st.write(f"**Selected {label}:**")
        for i, item in enumerate(st.session_state[session_key]):
            c1, c2 = st.columns([5, 1])
            c1.caption(item["label"])
            if c2.button("Remove", key=f"{session_key}_remove_{i}"):
                st.session_state[session_key].pop(i)
                st.rerun()

    return [item["id"] for item in st.session_state[session_key]]


# --- Books ---
st.subheader("Books you like")
book_ids = render_search_and_add("books", books_df, "title", "book_id", "reading_list")

# --- Authors ---
st.subheader("Authors you like")
author_ids = render_search_and_add("authors", authors_df, "name", "author_id", "author_list")

# --- Genres (small fixed set — multiselect is simpler than search+add) ---
st.subheader("Genres you like")
all_genres = genres_df["genres"].unique().tolist()
selected_genres = st.multiselect("Pick genres", all_genres, key="selected_genres")

# --- Pages and years (ranges) ---
st.subheader("Preferences")
p1, p2 = st.slider("Page count range", min_value=0, max_value=1500, value=(0, 1500), key="page_range")
y1, y2 = st.slider("Publication year range", min_value=1900, max_value=2026, value=(1900, 2026), key="year_range")

# --- Number of results + recommend button ---
st.subheader("Get recommendations")
st.write("How many book recommendations?")
col1, col2 = st.columns([3, 1])
if col1.button("Get Recommendations"):
    results = recomend_books.recommend_books(
        authors=author_ids,
        genres=st.session_state["selected_genres"],
        books=book_ids,
        pages=list(st.session_state["page_range"]),
        years=list(st.session_state["year_range"]),
        x=st.session_state["num_results"],
    )
    st.session_state["recommendations"] = results
num_results = col2.number_input("How many book recommendations?", min_value=1, max_value=50, value=10, step=1, key="num_results", label_visibility="collapsed")


# --- Divider between search criteria and results ---
st.divider()

# --- Display results ---
if "recommendations" in st.session_state:
    results = st.session_state["recommendations"]

    if results.empty:
        st.write("No matches found — try widening your search criteria.")
    else:
        for _, row in results.iterrows():
            col_img, col_info = st.columns([1, 3])

            with col_img:
                if pd.notna(row["image_url"]):
                    st.image(row["image_url"], width=150)
                else:
                    st.write("No cover available")

            with col_info:
                st.subheader(row["title"])
                if pd.notna(row["description"]):
                    st.write(row["description"])

                pages = int(row["num_pages"]) if pd.notna(row["num_pages"]) else "Unknown"
                year = int(row["publication_year"]) if pd.notna(row["publication_year"]) else "Unknown"
                genres_val = row["genres"]
                genres_display = ", ".join(genres_val) if isinstance(genres_val, list) else "Unknown"

                st.caption(f"By {row['authors']}")
                st.caption(f"{row['publisher']} · {year} · {pages} pages")
                st.caption(f"⭐ {row['average_rating']} ({row['ratings_count']} ratings)")
                st.caption(f"Genres: {genres_display}")

            st.divider()