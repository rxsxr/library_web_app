import streamlit as st
import mysql.connector 
from mysql.connector import Error

# connect to mySQL 
def create_connection():
    try:
        connection = mysql.connector.connect(
            host=st.secrets["database"]["DB_HOST"],
            user=st.secrets["database"]["DB_USER"],
            password=st.secrets["database"]["DB_PW"],
            database=st.secrets["database"]["DB_NAME"]
        )
        return connection
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None


def authenticate_user(login_id, pin): 
    connection = create_connection()
    if connection is None: 
        return None
    
    try: 
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT * 
            FROM Authentication 
            WHERE login_id = %s AND pin = %s 
            """
        cursor.execute(query, (login_id, pin))
        user = cursor.fetchone()
        connection.close()
        return user 
    except Error as e: 
        st.error(f"Error querying the database: {e}")
        return None




# ---------- functions for search ----------------

# execute search query based on parameters
def search_books(query, params=None):
    connection = create_connection()
    if connection is None:
        raise ConnectionError("Failed to connect to the database. Check your connection settings.")
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        return results
    except mysql.connector.Error as e:
        print(f"Error executing query: {e}")
        return []
    finally:
        if connection:
            connection.close()

# fetch all books based on parameter
def get_books_by_title(title):
    query = """
        SELECT b.book_title AS title, 
            a.first_name_a AS author_first_name, 
            a.last_name_a AS author_last_name, 
            b.year_published AS year_published, 
            bs.book_status_name AS book_status, 
            ba.age_group AS library_section, 
            bg.genre_name AS genre
        FROM Books b
        JOIN Authors a ON a.author_id = b.author_id
        JOIN BookStatus bs ON bs.book_status_id = b.book_status_id
        JOIN BookAge ba ON ba.age_id = b.age_id
        JOIN BookGenre bg ON bg.genre_id = b.genre_id
        WHERE b.book_title LIKE %s
    """
    return search_books(query, (f"%{title}%",))

# author full name 
def get_books_by_author(first_name, last_name):
    query = """
        SELECT b.book_title AS title, 
            a.first_name_a AS author_first_name, 
            a.last_name_a AS author_last_name, 
            b.year_published AS year_published, 
            bs.book_status_name AS book_status, 
            ba.age_group AS library_section, 
            bg.genre_name AS genre
        FROM Authors a
        JOIN Books b ON a.author_id = b.author_id
        JOIN BookStatus bs ON bs.book_status_id = b.book_status_id
        JOIN BookAge ba ON ba.age_id = b.age_id
        JOIN BookGenre bg ON bg.genre_id = b.genre_id
        WHERE a.first_name_a LIKE %s OR a.last_name_a LIKE %s
    """
    return search_books(query, (f"%{first_name, last_name}%",))


# author first name 
def get_books_by_author_first(first_name):
    query = """
        SELECT b.book_title AS title, 
            a.first_name_a AS author_first_name, 
            a.last_name_a AS author_last_name, 
            b.year_published AS year_published, 
            bs.book_status_name AS book_status, 
            ba.age_group AS library_section, 
            bg.genre_name AS genre
        FROM Authors a
        JOIN Books b ON a.author_id = b.author_id
        JOIN BookStatus bs ON bs.book_status_id = b.book_status_id
        JOIN BookAge ba ON ba.age_id = b.age_id
        JOIN BookGenre bg ON bg.genre_id = b.genre_id
        WHERE a.first_name_a LIKE %s
    """
    return search_books(query, (f"%{first_name}%",))


# author last name 
def get_books_by_author_last(last_name):
    query = """
        SELECT b.book_title AS title, 
            a.first_name_a AS author_first_name, 
            a.last_name_a AS author_last_name, 
            b.year_published AS year_published, 
            bs.book_status_name AS book_status, 
            ba.age_group AS library_section, 
            bg.genre_name AS genre
        FROM Authors a
        JOIN Books b ON a.author_id = b.author_id
        JOIN BookStatus bs ON bs.book_status_id = b.book_status_id
        JOIN BookAge ba ON ba.age_id = b.age_id
        JOIN BookGenre bg ON bg.genre_id = b.genre_id
        WHERE a.last_name_a LIKE %s
    """
    return search_books(query, (f"%{last_name}%",))


# ---------- functions for filter ----------------
def fetch_books(selected_categories, selected_ages, selected_genres, selected_status):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT b.book_title AS title, 
            a.first_name_a AS author_first_name, 
            a.last_name_a AS author_last_name, 
            b.year_published AS year_published, 
            bs.book_status_name AS book_status, 
            ba.age_group AS library_section, 
            bg.genre_name AS genre
        FROM Books b
        JOIN Authors a ON a.author_id = b.author_id
        JOIN BookCategory bc ON bc.category_id = b.category_id 
        JOIN BookStatus bs ON bs.book_status_id = b.book_status_id
        JOIN BookAge ba ON ba.age_id = b.age_id
        JOIN BookGenre bg ON bg.genre_id = b.genre_id
        WHERE 1=1
        """
    params = []

    if selected_categories: 
        query += " AND bc.category_name IN (%s)" % (", ".join(["%s"] * len(selected_categories)))
        params.extend(selected_categories)

    if selected_ages:  # Filter by age groups
        query += " AND ba.age_group IN (%s)" % (", ".join(["%s"] * len(selected_ages)))
        params.extend(selected_ages)
    
    if selected_genres:  # Filter by book genre
        query += " AND bg.genre_name IN (%s)" % (", ".join(["%s"] * len(selected_genres)))
        params.extend(selected_genres)

    if selected_status: # Filter by book status 
        query += " AND bs.book_status_name IN (%s)" % (", ".join(["%s"] * len(selected_status)))
        params.extend(selected_status)

    cursor.execute(query, params) 
    books = cursor.fetchall()
    connection.close()
    return books

