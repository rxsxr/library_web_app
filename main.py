import streamlit as st
from database import authenticate_user, get_books_by_title, get_books_by_author, get_books_by_author_first, get_books_by_author_last, fetch_books

# initialize the page state in session_state if it doesn't exist
if "page" not in st.session_state: 
    st.session_state.page = "home"

if "logged_in_patron" not in st.session_state:
    st.session_state.logged_in_patron = False
    st.session_state.patron_id = None

if "logged_in_staff" not in st.session_state:
    st.session_state.logged_in_staff = False
    st.session_state.staff_id = None


# function to go to a new page (by updating session_state)
def go_to_browse_page():
    st.session_state.page = "Browse the Catalogue"

def go_to_home():
    st.session_state.page = "home"
    st.rerun()

def go_to_search_page():
    st.session_state.page = "Search in Catalogue"

def go_to_filter_page():
    st.session_state.page = "Filter the Catalogue"

def go_to_signin_page():
    st.session_state.page = "Sign In"

def go_to_patron_page():
    st.session_state.page = "patron_account"

def go_to_staff_page():
    st.session_state.page = "staff_account"


# --------- filtering functions -----------
categories = ["Fiction", "Non-Fiction"]
age_groups = ["Kids", "Preteen", "YA", "Adult (18+)"]
genres = ["Mystery", "Romance", "Fantasy", "Sci-fi", "Thriller", "Horror"]
status = ["On Shelf", "Returned", "Checked-out", "Reserved"]
age_groups_dict = {
    "Kids (age 1-9)": "Kids",
    "Preteen (10-12)": "Preteen", 
    "YA (13-18)": "YA", 
    "Adult (18+)": "Adult"
}
status_dict = {
    "On Shelf": "on_shelf", 
    "Returned": "checked_out", 
    "Checked-out": "returned_pile", 
    "Reserved": "reserved"
}


# ----------- home page --------------- 
if st.session_state.page == "home":

    # top container 
    with st.container():
        top_left, top_right = st.columns([0.8, 0.2], vertical_alignment='center')
        with top_left:
            st.write("### Welcome to Thunder Bay's")
            st.write('''# Digital Library Catalogue''')
        with top_right: 
            sign_in_button = st.button("Sign In")
            if sign_in_button:
                go_to_signin_page()

    # middle container
    with st.container(): 
        browse_catalogue_button = st.button("Browse the Catalogue", use_container_width=True)
        if browse_catalogue_button:
            go_to_browse_page()
    

    # bottom container
    with st.container(): 
        st.image("books_image.jpg")


# ----------- browse page ---------------
elif st.session_state.page == "Browse the Catalogue":
    
    with st.container(): # webpage title
        st.write("Thunder Bay's Digital Library Catalogue")
    
    with st.container(): # webpage subtitle & home button
        left, right = st.columns([0.8, 0.2])

        with right: 
            home_button1 = st.button("Home", key="home1")
            if home_button1:
                go_to_home()

        with left: 
            st.title("Browse the Catalogue")
    
    with st.container():
        search_catalogue_button = st.button("Search in Catalogue")
        filter_catalogue_botton = st.button("Filter the Catalogue")
        

        # Implementing the search logic
        if search_catalogue_button:
            go_to_search_page()
        if filter_catalogue_botton:
            go_to_filter_page()

# ----------- search page --------------- 
elif st.session_state.page == "Search in Catalogue":
    with st.container(): # webpage title
        st.write("Thunder Bay's Digital Library Catalogue")

    with st.container():
        left, right = st.columns([0.8, 0.2])
        with right: 
            home_button2 = st.button("Home", key="home2")
            go_back_button1 = st.button("Prev Page", key="back1")
            if go_back_button1:
                go_to_browse_page()
            if home_button2:
                go_to_home()
        with left: 
            st.title("Browse the Catalogue")
            st.divider()
    
    with st.container():
        st.write(" ### Search in Catalogue")
        st.write("Note: leave blank if field is unknown")
        title_input = st.text_input("Enter title:")
        author_first_input = st.text_input("Enter author's first name:")
        author_last_input = st.text_input("Enter author's last name:")
        
        results = None

        if st.button("Search", key="search_button_1"):

            # if only title is given  
            if (title_input and author_first_input == "" and author_last_input == ""):
                results = get_books_by_title(title_input)

            # if only author first name is given  
            elif (author_first_input and author_last_input == "" and title_input == ""):
                results = get_books_by_author_first(author_first_input)
            
            # if only author last name is given 
            elif (author_first_input == "" and author_last_input and title_input == ""):
                results = get_books_by_author_last(author_last_input)

            # if only author first and last name are given: 
            elif (author_first_input and author_last_input and title_input == ""):
                results = get_books_by_author(author_first_input, author_last_input)

            # if all are given: 
            elif (author_first_input and author_last_input and title_input):
                results = get_books_by_author(author_first_input, author_last_input, title_input)
            
            # if none are entered  
            else: 
                results = []

        if results:
            st.write("Search Results:")
            for book in results: 
                    
                st.markdown(f"""
                <div style="
                    border: 1px solid #ddd; 
                    border-radius: 10px; 
                    padding: 15px; 
                    margin-bottom: 10px;
                    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1); 
                    background-color: #21314f;">
                    <h5>📚 {book['title']}</h4>
                    <div style="display: flex; gap: 175px;">
                        <div style="display: flex: 1;">
                            <p><strong>Author:</strong> {book['author_first_name']} {book['author_last_name']}</p>
                            <p><strong>Published:</strong> {book['year_published']}</p>
                            <p><strong>Status:</strong> {book['book_status']}</p>
                        </div>
                        <div style="display: flex: 1;">
                            <p><strong>Library Section:</strong> {book['library_section']}</p>
                            <p><strong>Genre:</strong> {book['genre']}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        elif results == []:
            st.write("No books found matching the given criteria.")
        else: 
            st.write("...")


# ----------- filter page --------------- 
elif st.session_state.page == "Filter the Catalogue":
    with st.container(): # webpage title
        st.write("Thunder Bay's Digital Library Catalogue")

    with st.container():
        left, right = st.columns([0.8, 0.2])
        with right: 
            home_button3 = st.button("Home", key="home3")
            go_back_button2 = st.button("Prev Page", key="back2")
            if go_back_button2:
                go_to_browse_page()
            if home_button3:
                go_to_home()
        with left: 
            st.title("Browse the Catalogue")
            st.divider()
    
    with st.container():
        st.write(" ### Filter the Catalogue")

        selected_categories = st.multiselect("Category", ["Fiction", "Non-Fiction"])
        selected_ages_1 = st.multiselect("Age", ["Kids (age 1-9)", "Preteen (10-12)", "YA (13-18)", "Adult (18+)"])
        selected_ages_2 = [age_groups_dict[age] for age in selected_ages_1]
        selected_genres = st.multiselect("Genre", ["Mystery", "Romance", "Fantasy", "Sci-fi", "Thriller", "Horror"])
        selected_status_1 = st.multiselect("Book Status", ["On Shelf", "Returned", "Checked-out", "Reserved"])
        selected_status_2 = [status_dict[status] for status in selected_status_1]
        
        if st.button("Apply Filters"):

            filtered_books = fetch_books(selected_categories, selected_ages_2, selected_genres, selected_status_2)

            if filtered_books: 
                for book in filtered_books: 
                    st.markdown(f"""
                <div style="
                    border: 1px solid #ddd; 
                    border-radius: 10px; 
                    padding: 15px; 
                    margin-bottom: 10px;
                    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1); 
                    background-color: #21314f;">
                    <h5>📚 {book['title']}</h4>
                    <div style="display: flex; gap: 175px;">
                        <div style="display: flex: 1;">
                            <p><strong>Author:</strong> {book['author_first_name']} {book['author_last_name']}</p>
                            <p><strong>Published:</strong> {book['year_published']}</p>
                            <p><strong>Status:</strong> {book['book_status']}</p>
                        </div>
                        <div style="display: flex: 1;">
                            <p><strong>Library Section:</strong> {book['library_section']}</p>
                            <p><strong>Genre:</strong> {book['genre']}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else: 
                st.write("No books match the selected filters.")

# ----------- sign-in page --------------- 
elif st.session_state.page == "Sign In":
    with st.container():
        st.write("Thunder Bay's Digital Library Catalogue")

    with st.container():
        left, right = st.columns([0.8, 0.2])
        with right: 
            home_button4 = st.button("Home", key="home4")
            if home_button4:
                go_to_home()
        with left: 
            st.title("Sign In")
            st.divider()

    with st.container():
        with st.form("Sign In", clear_on_submit=True):
            login_id = st.text_input("Login ID")
            pin = st.text_input("PIN", type="password")
            submitted = st.form_submit_button("Submit")
                
            if submitted: 
                user = authenticate_user(login_id, pin)
                        
                if user: 
                    st.success(f"Welcome, {user['login_id']}!")

                    if login_id.startswith("S"):
                        st.info("You are signed in as Staff.")
                        st.session_state.logged_in_staff = True
                        st.rerun()
                    elif login_id.startswith("L"):
                        st.info("You are signed in as Patron.")
                        st.session_state.logged_in_patron = True
                        st.rerun()
                else:
                    st.error("Invalid Login ID or PIN. Please try again.")
   
    with st.container():
        if st.session_state.logged_in_patron:
            if st.button("Go to My Account"):
                go_to_patron_page()

elif st.session_state.page == "patron_account":
    st.write("Welcome Patron!")
    if st.button("Log out"):
        st.session_state.logged_in_patron = False
        go_to_home()

elif st.session_state.page == "staff_account":
    st.write("Welcome Staff!")
    if st.button("Log out"):
        st.session_state.logged_in_patron = False
        go_to_home()
