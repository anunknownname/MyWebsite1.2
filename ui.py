from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime
with sqlite3.connect("database.db", check_same_thread=False) as database:
    db=database.cursor()

    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/checkout', methods=['POST','GET'])
    def user_checkout():
        user_data=request.form.get('user')
        passcode_data=request.form.get('passcode')
        
        # db.execute(f"SELECT user_pin FROM user WHERE user_name == '{user_data}'") #Getting the user pin from the name of the user
        # results = db.fetchall()
        # if results[0][0] == passcode_data:
        #     db.execute(f"SELECT user_name FROM user WHERE current_book IS NULL AND user_name == '{user_data}'") #Checking to see if the user is in the database and does not have a book out
        #     results = db.fetchall()
        #     if results:
        #         check_out() 
        #     else:
        #         db.execute(f"SELECT user_name FROM user WHERE user_name == '{user_data}'") #Searching to see whether the user is in the databse. If they are, because of the prior query, we know that they have a book out, else, they must not be in the database at all
        #         results = db.fetchall()
        #         if not results: #If the user doesn't exist in the database, ask them what they would like to do.
        #             print("go sign up")

        #         else:
        #             print("Looks like you already have a book out\nReturn your current book to be able to check a new one out.")
            
    

        # def check_out():
        #     db.execute(f"SELECT title FROM book_information WHERE title == '{book_name}' AND book_availability_status == 'Available'") #Using a query to check whether a book exists by seeing if it has data when searched using an SQL query
        #     results = db.fetchall()
        #     if results:
        #         db.execute(f"SELECT id FROM user WHERE user_name == '{user_data}'") #Finding the id of a user whos name has been passed into the function
        #         results = db.fetchall()
        #         user_id = results[0][0]
        #         db.execute(f"UPDATE user SET current_book = '{book_name}', borrowed_date = '{datetime.now()}' WHERE user_name == '{user_data}'") #Checking out the book using an UPDATE query
        #         db.execute(f"UPDATE book_information SET book_availability_status = 'Unavailable', current_user_id = '{user_id}' WHERE title == '{book_name}'")#Updating the books data to match the new user
        #         database.commit()
        #         print(f"You checked out {book_name}!")
        #     else:
        #         print("That book either doesn't exist, or it isn't available right now. Check your spelling.")
        #         database.commit()
            
         
        
        return render_template('checkout.html', user=user_data)



    @app.route('/library', methods=['POST', 'GET'])
    def library():
        availability=''
        data=[]
        results=[]
        none=''
        blurb=''
        search_results=''
        if request.method=='POST':
            data=request.form.get("search")
            if request.form.get("availability") == None:
                availability=''
            else:
                availability='Availabl'
           
            db.execute(f'''SELECT title, book_availability_status, genre, image_file_path, blurb, book_id FROM book_information JOIN author ON book_information.author_id = author.id WHERE book_availability_status LIKE '{availability}%' AND (author.name = "{data}"  OR genre = "{data}" OR title = "{data}");''')

            results=db.fetchall()
            print(results)
            if data == '' and results == []:
                db.execute(f'''SELECT title, book_availability_status, genre, image_file_path, blurb, book_id, author.name FROM book_information JOIN author ON book_information.author_id = author.id WHERE book_availability_status LIKE '{availability}%';''')
                results=db.fetchall()
            if results:
                none = ''
                search_results='Here are your results!'
            else:
                none ='There were no results :('
                search_results=''
                results=''
           
            
            
        return render_template('library.html', books=results, noresults=none, blurb=blurb, search_results=search_results)

    @app.route('/book/<int:book_id>')
    def book(book_id):
        db.execute(f'''SELECT title, book_availability_status, genre, image_file_path, blurb, book_id, author.name FROM book_information JOIN author ON book_information.author_id = author.id WHERE book_id = {book_id};''')
        results=db.fetchall()
        print(results)
        return render_template('book_info.html', results=results)
        
    @app.route("/book/<int:book_id>")
    def checkout(book_id):
        db.execute(f'''SELECT title, book_availability_status, genre, image_file_path, blurb, book_id, author.name FROM book_information JOIN author ON book_information.author_id = author.id WHERE book_id = {book_id};''')
        results=db.fetchall()
        return render_template('checkout.html', results=results)
    
    @app.route("/about")
    def about():
        return render_template('about.html')
    
    @app.route("/events")
    def events():
        return render_template('events.html')
    
    @app.route("/contact")
    def contact():
        return render_template('contact.html')

    @app.route("/login")
    def login():
        return render_template('login.html')
    
    @app.post('/availability')
    def availability_check():
        data=request.form.get("availability")

        return redirect("/availability")




if __name__ == '__main__':
    app.run(debug=True) 