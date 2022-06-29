import os

from flask import Flask, render_template, url_for, redirect, request  # import flask
import pandas as p
import tools as tls
import forms
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
p.options.mode.chained_assignment = None

app = Flask(__name__)

app.config["SECRET_KEY"] = "mysecretkey"


# login page
@app.route('/', methods=['GET', 'POST'])
def login():
    library_data = p.read_csv('csvfile.csv', encoding='utf-8')  # read data
    form = forms.Loginform()
    # when users click submit in the form
    if request.method == 'POST':
        # if login data is valid (f.e.: if it is in the CSV file)
        if form.validate_on_submit():
            # user is logged in and taken to the homepage
            tls.reset_basket()
            username = request.form['username']  # we get username information
            id_list = library_data["Id"].tolist()  # we get library information
            length_of_list = len(library_data)  # we get library information
            tls.reset_basket() # reset the user basket
            return render_template('personal.html', username=username, library_data=library_data,
                                   length_of_list=length_of_list, id_list=id_list, search_string=False)
        # if login data is not valid
        else:
            return render_template('login.html', form=form)  # redirect to login again
    # when users enter the page from the URL
    else:
        return render_template('login.html', form=form)


# homepage
@app.route('/personal', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        username = request.form["username"]  # take the username
        library_data = p.read_csv('csvfile.csv', encoding='utf-8')  # read data
        id_list = library_data["Id"].tolist()  # get library data
        length_of_list = len(library_data)  # get library data
        return render_template('personal.html', username=username, library_data=library_data,
                               length_of_list=length_of_list, id_list=id_list, search_string=False)

    return redirect(url_for("login"))


@app.route('/personal/search', methods=['POST'])
def personal():
    # take information from html
    filter_value = request.form["filter_value"]
    search_string = request.form["search"]

    # filter by books/author/category
    if filter_value == "1":
        search_list = tls.find_books(search_string)

    elif filter_value == "2":
        search_list = tls.find_author(search_string)

    elif filter_value == "3":
        search_list = tls.find_category(search_string)

    search_id_list = search_list["Id"].tolist()  # get the books
    username = request.form["username"]  # take the username
    length_of_list = len(search_list)
    return render_template('personal.html', library_data=search_list, username=username, length_of_list=length_of_list,
                           id_list=search_id_list, search_string=search_string, filter_value=filter_value)


@app.route('/register', methods=['GET', 'POST'])
def register():  # put application's code here
    # getting form information from RegisterForm
    form = forms.RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        name = form.name.data
        email = form.email.data
        matriculation = form.matriculation.data
        gender = form.gender.data
        birthdate = form.birth_date.data
        street_number = form.street.data
        postcode = form.postcode.data
        city = form.city.data

        # create new user
        new_user = {
            "Username": username,
            "Password": password,
            "Email": email,
            "Matriculation": matriculation,
            "Name": name,
            "Gender": gender,
            "Birthdate": birthdate,
            "Street Number and Name": street_number,
            "Postcode": postcode,
            "City": city,
            "Book History": "a",
            "Currently Rented": "a",
            "Picture Path": "default.png"
        }

        # add user to CSV
        tls.add_user(new_user)

        return redirect(url_for('login'))

    return render_template("register.html", form=form)


# adding to the cart
@app.route('/card', methods=['POST'])
def card():
    library_data = p.read_csv('csvfile.csv', encoding='utf-8')  # read data
    card_data = p.read_csv('usercard.csv', encoding='utf-8')

    if request.method == 'POST':
        # when user clicks add to cart button
        username = request.form['username']
        search_string = ""
        # if search_string == False:
        #     search_string = ""

        # taking book id
        id = request.form['id']

        search_list = tls.find_books(search_string)
        search_id_list = search_list["Id"].tolist()

        # how many items in the basket?
        item_count = tls.find_frequency(card_data, username)

        # book information
        length_of_list = int(request.form['length_of_list'])

        if int(id) > 0:
            # create a new variable to create basket
            usercard = {
                'Username': username,
                'Items': id,
            }

            usercard_data = p.read_csv('usercard.csv', encoding='utf-8')

            identical = False
            # if it exists in the usercard.csv
            # disallows user from adding the same book to the cart twice
            for index, row in usercard_data.iterrows():
                if row['Username'] == username and row['Items'] == int(id):
                    identical = True
            # add books to usercard.csv
            if not identical:
                usercard_data = usercard_data.append(usercard, ignore_index=True)
                usercard_data.to_csv('usercard.csv', encoding='utf-8', index=False)

        return render_template('personal.html', username=username, id=id, library_data=library_data,
                               item_count=item_count, length_of_list=length_of_list, id_list=search_id_list,
                               search_string=search_string)
    return render_template("personal.html")


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    # when user clicks the checkout button
    if request.method == 'POST':
        library_data = p.read_csv('csvfile.csv', encoding='utf-8')  # read data
        card_data = p.read_csv('usercard.csv', encoding='utf-8')  # read data
        username = request.form["username"]
        item_count = tls.find_frequency(card_data, username)

        # taking information from user card with a given username
        book_id_list = tls.user_card_items(username)
        # creating index for the book_id_list
        book_id_list_len = [i for i in range(len(book_id_list))]

        return render_template("checkout.html", library_data=library_data, username=username, item_count=item_count,
                               book_id_list=book_id_list, book_id_list_len=book_id_list_len)

    return redirect(url_for("login"))


@app.route('/checkout/delete', methods=['POST'])
def delete_item():
    # when user clicks on the delete button
    if request.method == 'POST':
        # reading csv
        library_data = p.read_csv('csvfile.csv', encoding='utf-8')  # read data
        card_data = p.read_csv('usercard.csv', encoding='utf-8')  # read data

        # getting information from HTML
        username = request.form["username"]
        id = request.form["id"]

        # removing the book from the csv file and resetting the book index
        card_data = card_data.drop(int(id)).reset_index(drop=True)

        # save
        card_data.to_csv('usercard.csv', encoding='utf-8', index=False)

        item_count = tls.find_frequency(card_data, username)

        book_id_list = tls.user_card_items(username)
        book_id_list_len = [i for i in range(len(book_id_list))]

        id_list_str = ""

        return render_template("checkout.html", library_data=library_data, username=username, item_count=item_count,
                               book_id_list=book_id_list, book_id_list_len=book_id_list_len,
                               book_id_list_str=id_list_str)

    return render_template("checkout.html")


@app.route('/completed', methods=['POST'])
# when user clicks on the checkout button
def completed():
    username = request.form["username"]
    # finds all books in the basket from a given username
    book_id_list = tls.user_card_items(username)
    # takes the book(s) in the cart and decreases the number of copies in the csvfile by one
    tls.borrow_book(book_id_list)
    # resets the user cart
    tls.user_card_reset(username)

    # takes the book(s) and adds them to the user history
    tls.borrow_to_user(username, book_id_list)

    library_data = p.read_csv('csvfile.csv', encoding='utf-8')  # read data
    id_list = library_data["Id"].tolist()
    length_of_list = len(library_data)
    return render_template('personal.html', library_data=library_data, username=username, id_list=id_list,
                           length_of_list=length_of_list)


@app.route('/profile/<username>', methods=['POST'])
def profile(username):
    username = request.form["username"]
    library_data = p.read_csv('csvfile.csv', encoding='utf-8')  # read data
    # finds the user data from a given username
    name = tls.find_username_data("Name", username)
    email = tls.find_username_data("Email", username)
    matriculation = tls.find_username_data("Matriculation", username)
    gender = tls.find_username_data("Gender", username)
    birthdate = tls.find_username_data("Birthdate", username)
    street_number = tls.find_username_data("Street Number and Name", username)
    postcode = tls.find_username_data("Postcode", username)
    city = tls.find_username_data("City", username)
    profile_picture = tls.find_username_data("Picture Path", username)
    rented_books = tls.get_rented_books(username)
    book_history = tls.get_book_history(username)

    return render_template("profile.html", name=name, email=email, matriculation=int(matriculation), gender=gender,
                           birthdate=birthdate, street_number=street_number, postcode=int(postcode), city=city,
                           rented_books=rented_books, library_data=library_data, username=username,
                           book_history=book_history, profilePicture=profile_picture)


@app.route('/returned', methods=['POST'])
# when user clicks on the return button
def returned():
    username = request.form["username"]
    book_id = request.form["book_id"]
    # increases number of copies in the csv file by one
    tls.increase_copy(int(book_id))

    library_data = p.read_csv('csvfile.csv', encoding='utf-8')  # read data
    length_of_list = len(library_data)
    id_list = library_data["Id"].tolist()

    # adds returned book to the user history in the CSV file
    tls.return_book(username, book_id)

    return render_template('personal.html', library_data=library_data, username=username, book_id=book_id,
                           length_of_list=length_of_list, id_list=id_list)


@app.route("/stats", methods=["POST"])
def statistics():
    username = request.form["username"]
    # getting statistics for the category
    stats = tls.get_statistics(0)

    genre = ["Arts & Photographies"]

    # getting overall statistics
    overall = tls.overall_statistics()

    return render_template("stats.html", stats=stats, genre=genre, genre_id=0, overall=overall, username=username)


@app.route("/stats/category", methods=["POST"])
def cat_stats():
    username = request.form["username"]
    # getting the category value from HTML
    genre_id = request.form["genre_id"]
    overall = tls.overall_statistics()

    genre = ["Arts & Photographies", "Biographies & Memoirs", "Business & Money", "Calendars", "Children's Books",
             "Comics & Graphic Novels", "Computers & Technology", "Cookbooks, Food & Wine", "Crafts, Hobbies & Home",
             "Christian Books & Bibles", "Engineering & Transportation"]

    # filtering the stats based on the given genre_id
    if genre_id == "0":
        stats = tls.get_statistics(0)
    elif genre_id == "1":
        stats = tls.get_statistics(1)
    elif genre_id == "2":
        stats = tls.get_statistics(2)
    elif genre_id == "3":
        stats = tls.get_statistics(3)
    elif genre_id == "4":
        stats = tls.get_statistics(4)
    elif genre_id == "5":
        stats = tls.get_statistics(5)
    elif genre_id == "6":
        stats = tls.get_statistics(6)
    elif genre_id == "7":
        stats = tls.get_statistics(7)
    elif genre_id == "8":
        stats = tls.get_statistics(8)
    elif genre_id == "9":
        stats = tls.get_statistics(9)
    elif genre_id == "10":
        stats = tls.get_statistics(10)

    return render_template("stats.html", stats=stats, genre=genre, genre_id=int(genre_id), overall=overall,
                           username=username)


@app.route("/uploaded", methods=["POST"])
def uploaded():
    # user uploads a picture
    username = request.form["username"]
    profile_picture = request.files["profilePicture"]
    if profile_picture:
        # setting a name for the picture
        file_name = f"{username}_picture"
        # saving the picture
        profile_picture.save(os.path.join("static/images", file_name))
        # saving the picture name to the CSV
        tls.save_profile_picture(username, file_name)
    else:
        return redirect(url_for('profile', username=username))

    library_data = p.read_csv('csvfile.csv', encoding='utf-8')
    length_of_list = len(library_data)
    id_list = library_data["Id"].tolist()

    return render_template('personal.html', library_data=library_data, username=username,
                           length_of_list=length_of_list, id_list=id_list)


if __name__ == '__main__':
    app.run()
