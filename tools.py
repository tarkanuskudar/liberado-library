import pandas as p


def borrow_book(book_id_list):  # 20
    # this is reading the csv file to figure out how many copies of the book there are.
    for book_id in book_id_list:
        library_data = p.read_csv('csvfile.csv')  # read data
        # if the number of copies is >=1, then a copy will be subtracted when a user borrows a book.
        if (library_data['Copies'][book_id] >= 1):
            library_data['Copies'][book_id] -= 1
        # this saves the information
        library_data.to_csv('csvfile.csv', encoding='utf-8', index=False)  # saving


def add_user(new_user):
    # this is how a new user is added to the csv file
    # read
    user_data = p.read_csv('user.csv')
    # update
    user_data = user_data.append(new_user, ignore_index=True)
    # save
    user_data.to_csv('user.csv', encoding='utf-8', index=False)


def check_register(data):
    # this is how to check if a username and password exist
    user_data = p.read_csv('user.csv')
    if data in user_data.values:
        return True
    else:
        return False


def check_login_username(username):
    user_data = p.read_csv('user.csv')
    if username in user_data.Username.values:
        return True
    else:
        return False


def check_login_password(username, password):
    # check if the username and the password are on the same row.
    user_data = p.read_csv('user.csv')
    user_data = user_data[(user_data['Username'] == username) & (user_data["Password"] == password)]
    if user_data.__len__() > 0:
        return True
    else:
        return False


def find_frequency(df, username):
    # this shows how many books are in a checkout basket
    count = 0
    for user in df["Username"]:
        if user == username:
            count += 1
    return count


def user_card_items(username):
    # bringing the book ids from a given username from the usercard.csv and putting them in a list and returning
    card_data = p.read_csv('usercard.csv')
    index_list = []
    id_list = []
    index = 0

    # find the given username in the csv file
    for user in card_data['Username']:
        if user == username:
            index_list.append(index)
        index += 1

    # add items to the id_list
    for i in index_list:
        id_list.append(card_data["Items"][i])

    return id_list  # [23, 6]


def user_card_reset(username):
    # when user clicks checkout we need to reset the user basket on the CSV file
    card_data = p.read_csv('usercard.csv')
    card_data = card_data[card_data["Username"].str.contains(username) == False]
    card_data.to_csv('usercard.csv', encoding='utf-8', index=False)


def capitalize_first_letter(string):
    # These are the search field parameters. They include the function to capitalize the
    # first letter of each Title and author so as to match the csv file.
    x = string.split()
    return ' '.join([i.capitalize() for i in x])


def find_books(search_string):
    # when the user inputs information as search string, finds and returns the results under the book title
    search_string = capitalize_first_letter(search_string)
    library_data = p.read_csv('csvfile.csv')  # read data
    result_data = library_data[library_data["Title"].str.contains(search_string)]
    return result_data


def find_author(search_string):
    # when the user inputs information as search string, finds and returns the results under the author name
    search_string = capitalize_first_letter(search_string)
    library_data = p.read_csv('csvfile.csv')  # read data
    library_data = library_data.fillna("Unknown")
    result_data = library_data[library_data["Author(s)"].str.contains(search_string)]
    return result_data


def find_category(search_string):
    # when the user inputs information as search string, finds and returns the results under the category name
    search_string = capitalize_first_letter(search_string)
    library_data = p.read_csv('csvfile.csv')  # read data
    result_data = library_data[library_data["Genre"].str.contains(search_string)]
    return result_data


def find_username_data(data_type, username):
    # finds the user data from the user.csv with a given data type(for example, name, email, matriculation, address)
    user_data = p.read_csv('user.csv', encoding='utf-8')  # read data
    return user_data[data_type].where(user_data['Username'] == username).dropna().values[0]


def borrow_to_user(username, list):
    # adds checked out book to the currently rented books in user.csv
    user_data = p.read_csv('user.csv', encoding='utf-8')  # read data
    index = user_data.index[user_data['Username'] == username].tolist()
    str_list = ' '.join(str(i) for i in list)
    user_data["Currently Rented"][index[0]] += " " + str_list
    user_data.to_csv('user.csv', encoding='utf-8', index=False)


def get_rented_books(username):
    # gets currently rented books from the user.csv with a given username
    user_data = p.read_csv('user.csv', encoding='utf-8')  # read data
    index = user_data.index[user_data['Username'] == username].tolist()
    string_books = user_data["Currently Rented"][index[0]]
    list_books = list(string_books.split(" "))
    list_books.pop(0)
    return list_books


def get_book_history(username):
    # gets book rental history from the user.csv with a given username
    user_data = p.read_csv('user.csv', encoding='utf-8')  # read data
    index = user_data.index[user_data['Username'] == username].tolist()
    string_books = user_data["Book History"][index[0]]
    list_books = list(string_books.split(" "))
    list_books.pop(0)
    return list_books


def return_book(username, id):
    # returns book with a given id and username
    user_data = p.read_csv('user.csv', encoding='utf-8')  # read data
    index = user_data.index[user_data['Username'] == username].tolist()  # find index
    string_books = user_data["Currently Rented"][index[0]]  # get data as string
    list_books = list(string_books.split(" "))  # convert data to list
    list_books.remove(str(id))  # remove data from list
    str_list = ' '.join(str(i) for i in list_books)  # convert to str again
    user_data["Currently Rented"][index[0]] = str_list
    # add to history
    user_data["Book History"][index[0]] += " " + id
    user_data.to_csv('user.csv', encoding='utf-8', index=False)


def get_statistics(genre_id):
    # get statistics for a given genre_id via pandas
    library_data = p.read_csv('csvfile.csv', encoding='utf-8')  # read data
    stat_data = library_data[library_data["Genre ID"] == genre_id]
    stat_data = stat_data["Rating"]
    return stat_data.describe()


def overall_statistics():
    # get overall statistics
    library_data = p.read_csv('csvfile.csv', encoding='utf-8')  # read data
    stat_data = library_data["Rating"]
    return stat_data.describe()


def increase_copy(book_id):
    # increase the copy of the given book on the csvfile
    library_data = p.read_csv('csvfile.csv', encoding='utf-8')  # read data
    library_data['Copies'][book_id] += 1
    library_data.to_csv('csvfile.csv', encoding='utf-8', index=False)  # saving


def save_profile_picture(username, picture_name):
    user_data = p.read_csv('user.csv', encoding='utf-8')  # read data
    index = user_data.index[user_data['Username'] == username].tolist()
    user_data["Picture Path"][index[0]] = picture_name
    user_data.to_csv('user.csv', encoding='utf-8', index=False)  # saving


def reset_basket():
    user_basket = p.read_csv('usercard.csv', encoding='utf-8')  # read data
    user_basket = user_basket.iloc[0:0]
    user_basket.to_csv('usercard.csv', encoding='utf-8', index=False)  # saving
