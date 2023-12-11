# PROGRAM TO CREATE A LIBRARY MANAGEMENT PROJECT USING SQLITE3 DATABASE

import sqlite3
import datetime as dt

con = sqlite3.connect("Library_database.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

# FOLLOWING QUERIES CREATES Student_info TABLE, Book_info TABLE, Book_history TABLE and Book_history TABLE

# con.execute('''
#       Create table Student_info (Stud_id INT (3), Stud_name VARCHAR (25), Stud_class VARCHAR (7))''')
# '''con.execute('''
#        Create table Book_info (Book_id INT (5), Book_name VARCHAR (25), Book_author VARCHAR (25),
#         Book_publication VARCHAR (20))
# con.execute('''
#        Create table Book_history (Book_id INT(5), Book_name VARCHAR (25), Stud_id INT(3), Issue_date TIMESTAMP,
#         Return_date TIMESTAMP)'''
#            " Issue_date TIMESTAMP, Return_date TIMESTAMP")


def check_student(student):                     # FUNCTION TO CHECK IF THE STUDENT IS PRESENT IN THE DATABASE OR NOT
    student_found = False
    connection = sqlite3.connect("Library_database.db")                 # TO CONNECT TO THE LIBRARY_DATABASE
    cursor_obj = connection.cursor()
    cursor_obj.execute("SELECT Stud_id, Stud_name from Student_info WHERE Stud_id = ?", (student,))
    # SELECT QUERY TO CHECK IF THE STUDENT IS PRESENT IN THE Student_info TABLE or not
    student_info = cursor_obj.fetchone()
    if student_info:
        student_found = True
        return student_found, student_info[1]           # RETURNS TRUE AND THE NAME OF THE STUDENT IF FOUND
    else:
        return student_found, 0                         # RETURNS FALSE IF THE STUDENT IS NOT FOUND


def check_book(book):                       # FUNCTION TO CHECK IF THE BOOK IS AVAILABLE IN THE LIBRARY OR NOT
    book_found = False
    connection = sqlite3.connect("Library_database.db")         # TO CONNECT TO THE LIBRARY_DATABASE
    cursor_obj = connection.cursor()
    cursor_obj.execute("SELECT Book_id, Book_name from Book_info WHERE Book_id = ?", (book,))
    # SELECT QUERY TO CHECK IF THE BOOK IS PRESENT IN THE Book_info TABLE OR NOT
    book_details = cursor_obj.fetchone()
    if book_details:
        book_found = True
        return book_found, book_details[1]              # RETURN TRUE AND THE NAME OF THE BOOK IF THE BOOK IS FOUND
    else:
        return book_found, 0                            # RETURNS FALSE IF THE BOOK IS NOT FOUND


def issue_book():                           # FUNCTION TO ISSUE A BOOK FROM THE LIBRARY
    student_id = input("\n\nENTER THE STUDENT ID : ")  # ENTER THE STUDENT ID WHO WANTS TO ISSUE A BOOK FROM THE LIBRARY
    student_found, student_name = check_student(student_id)     # CALLING TO check_student FUNCTION TO CHECK IF THE
    # STUDENT EXISTS IN THE DATABASE OR NOT
    if student_found:                                   # IF STUDENT IS FOUND IN THE DATABASE
        book_id = input("ENTER THE BOOK ID : ")         # ENTER THE ID OF THE BOOK TO ISSUE
        book_present, book_name = check_book(book_id)   # CALLING TO check_book FUNCTION TO CHECK IF THE BOOK
        # IS AVAILABLE AT THE LIBRARY AT THE OR NOT
        issued_date = str(dt.date.today())              # TO STORE THE ISSUE DATE
        if book_present:
            update_issued_books = ("INSERT into Book_history (book_id, book_name, Stud_id, Issue_date, Return_date)"
                                   "values (" + book_id + ",'" + book_name + "'," + student_id + ",'" + issued_date +
                                   "','" + "NA" + "'" ")")
            # UPDATE QUERY TO UPDATE THE DETAILS OF THE Book_hisory TABLE
            update_student_history = ("INSERT into Student_history (Stud_id, Stud_name, Book_name, Issue_date,"
                                      " Return_date) values (" + student_id + ",'" + student_name + "','" + book_name +
                                      "','" + issued_date + "','" + "NA" + "'" ")")
            # UPDATE QUERY TO UPDATE THE DETAILS OF TEH Student_history TABLE
            conn = sqlite3.connect("Library_database.db")               # TO CONNECT TO THE LIBRARY_DATABASE
            conn.execute(update_issued_books)
            conn.execute(update_student_history)
            conn.commit()
            conn.close()
            print("\n\n||", book_name, "HAS BEEN ISSUED TO", student_name, "||\n")  # DISPLAYS DETAILS OF THE BOOK NAME
            # AND THE STUDENT NAME WHICH HAS ISSUED THE BOOK
            input()
        else:                                   # DISPLAYS THE MESSAGE IF THE BOOK IS NOT AVAILABLE AT THE LIBRARY
            print("\n\n||BOOK IS NOT AVAILABLE AT THE LIBRARY||\n")
    else:                                       # DISPLAYS THE MESSAGE IF THE STUDENT IS NOT PRESENT IN THE LIBRARY
        print("\n\n||STUDENT IS NOT PRESENT IN THE DATABASE||\n")
    input()


def return_book():          # FUNCTION TO RETURN THE BOOK TO THE LIBRARY WHICH HAS BEEN ISSUED BY THE STUDENT
    stud_id = input("\n\nENTER THE STUDENT ID : ")          # ENTER THE STUDENT ID
    book_id = input("ENTER THE BOOK ID : ")                 # ENTER THE BOOK ID TO RETURN TO THE LIBRARY
    conn = sqlite3.connect("Library_database.db")           # TO CONNECT TO THE LIBRARY_DATABASE
    cursor = con.cursor()
    return_date = str(dt.date.today())
    cursor.execute("UPDATE Book_history set Return_date = '" + return_date + "'WHERE Book_id =" + book_id +
                   " and Return_date = 'NA'")
    # UPDATE QUERY TO UPDATE THE RETURN DATE IN THE Book_history table
    cursor.execute("UPDATE Student_history set Return_date = '" + return_date + "'WHERE Stud_id =" + stud_id +
                   " and Return_date = 'NA'")
    # UPDATE QUERY TO UPDATE THE RETURN DATE IN THE Student_history table
    con.commit()
    conn.close()
    print("\n||BOOK HAS BEEN SUCCESSFULLY RETURNED TO THE LIBRARY||\n")  # TO DISPLAY MESSAGE WHEN THE BOOK HAS BEEN
    # SUCCESSFULLY RETURNED TO LIBRARY
    input()


def book_history():      # FUNCTION TO DISPLAY HOW MANY TIMES THE BOOK HAS BEEN ISSUED AND RETURNED AND BY WHICH STUDENT
    book_id = input("\n\nENTER THE BOOK ID : ")               # ENTER THE BOOK ID OF WHICH THE USER WANTS TO SEE HISTORY
    connection = sqlite3.connect("Library_database.db")             # TO CONNECT TO THE LIBRARY_DATABASE
    cursor_obj = connection.cursor()
    cursor_obj.execute("SELECT * from Book_history WHERE book_id = ?", (book_id,))
    # SELECT QUERY TO SELECT THE SPECIFIC BOOK OF WHICH THE USER WANTS TO SEE HISTORY
    book_info = cursor_obj.fetchall()
    if book_info:                       # DISPLAYS THE BOOK HISTORY IF THE BOOK HAS BEEN ISSUED
        print("\n\n||BOOK_ID||\t\t||BOOK_NAME||\t\t||STUD_ID|\t\t||ISSUED_DATE||\t\t||RETURN_DATE||\n")
        for a, b, c, d, e in book_info:
            print(a, "\t\t\t", b, "\t\t", c, "\t\t\t", d, "\t\t\t", e)
            print()
    else:                               # DISPLAYS THE MESSAGE IF THE BOOK HAS NOT BEEN ISSUED YET
        print("\n\n||BOOK HAS NOT BEEN ISSUED FROM THE LIBRARY||")
    input()


def student_history():         # TO DISPLAY HOW MANY TIMES THE STUDENT HAS ISSUED AND RETURNED THE BOOK FROM THE LIBRARY
    student_id = input("\n\nENTER THE STUDENT ID : ")
    connection = sqlite3.connect("Library_database.db")                         # TO CONNECT TO THE LIBRARY_DATABASE
    cursor_obj = connection.cursor()
    cursor_obj.execute("SELECT * from Student_history WHERE Stud_id = ?", (student_id,))
    # SELECT QUERY TO SELECT THE SPECIFC STUDENT OF WHICH THE USER WANTS TO SEE THE HISTORY
    book_info = cursor_obj.fetchall()
    if book_info:                               # DISPLAYS THE STUDENT HISTORY IF FOUND
        print("\n\n||STUD_ID||\t\t||STUD_NAME||\t\t\t||BOOK_NAME|\t\t||ISSUED_DATE||\t\t||RETURN_DATE||\n")
        for a, b, c, d, e in book_info:
            print(a, "\t\t\t", b, "\t\t", c, "\t\t", d, "\t\t", e)
            print()
    else:                                       # DISPLAYS MESSAGE IF THE STUDENT HAS NOT ISSUED ANY BOOK YET
        print("\n\n||STUDENT HAS NOT TAKEN ANY BOOK FROM THE LIBRARY||")
    input()


def search_book():                                            # TO SEARCH TO DETAILS OF THE SPECFIC BOOK IN THE DATABASE
    book_id = input("\n\nENTER THE BOOK ID : ")               # ENTER THE BOOK ID TO SEARCH IN THE LIBRARY
    connection = sqlite3.connect("Library_database.db")       # TO CONNECT TO THE LIBRARY_DATABASE
    cursor_obj = connection.cursor()
    cursor_obj.execute("SELECT * from Book_info WHERE book_id = ?", (book_id,))
    # SELECT QUEREY TO SELECT THE SPECIFC WHICH DEPENDING UPON THE USER'S INPUT
    book_info = cursor_obj.fetchall()
    if book_info:                              # TO DISPLAY THE DETAILS OF THE BOOK IF BOOK IS AVAILABLE AT THE LIBRARY
        print("\n\n=============================================================================")
        print("||BOOK_ID||\t\t||BOOK_NAME||\t\t||BOOK_AUTHOR||\t\t||BOOK_PUBLICATION")
        print("=============================================================================\n")
        for a, b, c, d in book_info:
            print(a, "\t\t\t", b, "\t   ", c, "\t\t ", d)
            print()
    else:                                       # TO DISPLAY MESSAGE IF BOOK IS NOT AVAILABLE AT THE LIBRARY
        print("\n\n||BOOK IS NOT AVAILABLE AT THE LIBRARY||\n")
    input()


def add_new_book():                                         # TO ADD NEW BOOK IN THE LIBRARY
    book_id = input("\nENTER THE BOOK ID : ")               # ENTER THE NEW BOOK ID TO ADD IN THE Book_info table
    book_name = input("ENTER THE BOOK NAME : ")             # ENTER THE NEW BOOK NAME TO ADD IN THE Book_info table
    book_author = input("ENTER THE BOOK AUTHOR : ")     # ENTER THE NEW BOOK AUTHOR'S NAME TO ADD IN THE Book_info table
    book_publication = input("ENTER THE BOOK PUBLICATION : ")   # ENTER THE PUBLICATION NAME OF THE NEW BOOKS

    insert_book_data = ("insert into Book_info (Book_id , Book_name, Book_author, Book_publication) values (" + book_id
                        + ",'" + book_name + "','" + book_author + "','" + book_publication + "'" ")")
    # INSERT QUERY TO ADD THE DETAILS OF THE NEW BOOK IN THE Book_info table
    connect = sqlite3.connect("Library_database.db")        # TO CONNECT TO THE LIBRARY_DATABASE
    connect.execute(insert_book_data)
    connect.commit()
    connect.close()
    print("\n||NEW BOOK IS ADDED TO THE LIBRARY||\n")      # PRINT THE MESSAGE WHEN THE NEW BOOK IS ADDED TO THE LIBRARY
    input()


def add_new_student():                                       # TO ADD NEW STUDENT IN THE DATABASE
    student_id = input("\nENTER THE STUDENT ID : ")          # ENTER THE NEW STUDENT ID TO ADD IN THE DATABASE
    student_name = input("ENTER THE STUDENT NAME : ")        # ENTER THE NEW STUDENT NAME TO ADD IN THE DATABASE
    student_class = input("ENTER THE STUDENT CLASS : ")      # ENTER THE NEW STUDENT CLASS TO ADD IN THE DATABASE

    insert_new_student = ("insert into Student_info (Stud_id, Stud_name, Stud_class) values (" + student_id + ",'"
                          + student_name + "','" + student_class + "'" ")")     # INSERT QUERY TO ADD DETAILS OF THE
    # NEW STUDENT IN THE Stud_info TABLE
    connect = sqlite3.connect("Library_database.db")            # TO CONNECT TO THE LIBRARY_DATABASE
    connect.execute(insert_new_student)
    connect.commit()
    connect.close()
    print("\n|| NEW STUDENT IS ADDED TO THE DATABASE||\n")      # PRINT THE MESSAGE WHEN THE NEW STUDENT IS ADDED TO
    # THE Stud_info TABLE
    input()


def not_returned_book():
    connection = sqlite3.connect("Library_database.db")                 # TO CONNECT TO THE LIBRARY_DATABASE
    cur = connection.cursor()
    cur.execute("SELECT * from Book_history WHERE Return_date = ?", ("NA",))   # TO SELECT THE DETAILS
    # OF THE NOT RETURNED BOOKS
    unreturned_books = cur.fetchall()
    print("\n\n====================================================================================")
    print("||BOOK_ID||\t ||BOOK_NAME||\t\t||STUD_ID||\t\t||ISSUE_DATE||\t\t||RETURN_DATE||")
    print("====================================================================================\n")
    for a, b, c, d, e in unreturned_books:
        print(a, " \t\t", b, "\t\t", c, "\t\t\t", d, "\t\t\t", e)       # DISPLAY THE LIST OF NOT RETURNED BOOKS
        print()
    input()


def search_student():
    stud_id = input("\nENTER THE STUDENT ID : ")             # TO INPUT STUDENT ID FROM THE USER
    connection = sqlite3.connect("Library_database.db")      # TO CONNECT TO THE LIBRARY_DATABASE
    cursor_obj = connection.cursor()
    cursor_obj.execute("SELECT * from Student_info WHERE Stud_id = ?", (stud_id,))  # TO SELECT THE
    # STUDENT FROM THE Student_info WHOSE ID MATHCES WITH THE USER'S INPUT
    student_info = cursor_obj.fetchall()
    if student_info:
        print("\n\n=====================================================")
        print("||STUD_ID||\t\t||STUD_NAME||\t\t||STUD_CLASS||")
        print("=====================================================\n")
        for a, b, c in student_info:
            print(a, "\t\t\t", b, "\t\t  ", c)                  # TO DISPLAY THE INFORMATION OF THE STUDENT
            print()
    else:
        print("\n\n||STUDENT IS NOT PRESENT IN THE DATABASE||\n")   # IF THE ENTERED STUDENT ID IS NOT PRESENT
        # IN THE DATABASE
    input()


def show_all_issued_books():
    connection = sqlite3.connect("Library_database.db")                  # TO CONNECT TO THE LIBRARY_DATABASE
    cur = connection.cursor()                                          # TO SELECT ALL BOOKS FROM THE Book_history TABLE
    cur.execute("SELECT * from Book_history")
    all_issued_books = cur.fetchall()                   # TO SELECT ALL THE COLUMNS FROM THE SELECTED Book_history TABLE
    print("\n\n====================================================================================")
    print("||BOOK_ID||\t ||BOOK_NAME||\t\t||STUD_ID||\t\t||ISSUE_DATE||\t\t||RETURN_DATE||")
    print("====================================================================================\n")
    for a, b, c, d, e in all_issued_books:
        print(a, " \t\t", b, "\t\t", c, "\t\t\t", d, "\t\t\t", e)       # TO DISPLAY INFORMATION OF ALL ISSUED BOOKS
        print()
    input()


def show_library_books():
    connect = sqlite3.connect("Library_database.db")            # TO CONNECT TO THE LIBRARY_DATABASE
    cur = connect.cursor()
    cur.execute("SELECT * from Book_info")                      # TO SELECT ALL BOOKS FROM THE Book_info TABLE
    all_book_info = cur.fetchall()                         # TO SELECT ALL THE COLUMNS FROM THE SELECTED Book_info TABLE
    books_list = all_book_info
    print("\n\n================================================================================")
    print("||BOOK_ID||\t ||BOOK_NAME||\t\t||BOOK_AUTHOR||\t\t ||BOOK_PUBLICATION||")
    print("================================================================================\n")
    for a, b, c, d in books_list:
        print(a, " \t\t", b, "\t\t", c, "\t\t", d)                  # TO DISPLAY THE INFORMATION OF ALL THE BOOKS
        print()
    input()


while True:
    print("\n==============================================================")
    print("\t\t\t\t\t||WELCOME TO CENTRAL LIBRARY||\n==============================================================\n")
    print("1 - ISSUE BOOK")
    print("2 - RETURN BOOK")                     # CHOICES GIVEN TO THE USER TO PERFORM VARIOUS OPERATIONS
    print("3 - ADD NEW BOOK")
    print("4 - ADD NEW STUDENT")
    print("5 - SEARCH BOOK")
    print("6 - SEARCH STUDENT")
    print("7 - BOOK HISTORY")
    print("8 - STUDENT HISTORY")
    print("9 - SHOW NOT RETURNED BOOKS")
    print("10 - SHOW ALL ISSUED BOOKS")
    print("11 - SHOW ALL LIBRARY BOOKS")
    print("12  - EXIT\n")
    user_choice = int(input("PLEASE ENTER YOUR CHOICE : "))  # TO TAKE THE CHOICE FROM THE USER

    if user_choice == 1:
        issue_book()                                    # CALLING TO issue_book() FUNCTION TO ISSUE BOOKS TO THE STUDENT
    elif user_choice == 2:
        return_book()                              # CALLING TO return_book() FUNCTION TO RETURN THE BOOK TO THE LIBRARY
    elif user_choice == 3:
        add_new_book()                               # CALLING TO add_new_book() FUNCTION TO ADD NEW BOOK TO THE LIBRARY
    elif user_choice == 4:
        add_new_student()               # CALLING TO add_new_student() FUNCTION TO ADD NEW STUDENT DATA IN THE DATABASE
    elif user_choice == 5:
        search_book()                       # CALLING TO search_book() FUNCTION TO GIVE INFORMATION ABOUT A SPECFIC BOOK
    elif user_choice == 6:
        search_student()              # CALLING TO search_student() FUNCTION TO GIVE INFORMATION ABOUT A SPECIFC STUDENT
    elif user_choice == 7:
        book_history()                    # CALLING TO THE book_history() FUNCION TO DISPLAY THE HOW MANY TIMES BOOK HAS
        # BEEN ISSUED AND RETURNED AND THE BY WHICH STUDENT
    elif user_choice == 8:        # CALLLING TO THE student_history() FUNCTION TO DISPLAY HOW MANY TIMES THE STUDENT HAS
        # ISSUED AND RETURNED THE BOOK AND THE NAME OF THE ISSUED BOOK
        student_history()
    elif user_choice == 9:                  # CALLING TO THE not_returned_book() FUNCTION TO DISPLAY THE LIST OF BOOKS
        # WHICH HAS NOT BEEN RETURNED YET
        not_returned_book()
    elif user_choice == 10:                 # CALLING TO THE show_all_issued_book() FUNCTION TO DISPLAY THE LIST OF
        # ALL THE ISSUED BOOKS
        show_all_issued_books()
    elif user_choice == 11:
        show_library_books()          # CALLING TO THE show_library_books() FUNCTION TO DISPLAY THE INFORMATION OF
        # ALL THE BOOKS OF THE LIBRARY
    elif user_choice == 12:
        exit(0)                     # TO EXIT THE MENU
    else:
        print("\n||INVALID OPTION\n||PLEASE SELECT VALID OPTION||\n")       # DISPLAYS MESSAGE IF THE USERS SELECTS
        # INVALID OPTION
