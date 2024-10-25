from flask import Flask, render_template, request, redirect, url_for #Flask modules
import sqlite3 #Databasing
import datetime
with sqlite3.connect("database.db", check_same_thread=False) as database: #Connecting the database
    db=database.cursor()

    app = Flask(__name__)

    @app.route('/') #Rendering index.html
    def index():
        return render_template('index.html')

    #Everything Below is relevant code for future log in/checkout system

    # @app.route('/checkout', methods=['POST','GET'])
    # def user_checkout():
    #     print(a)
    #     user_data=request.form.get('user')
    #     passcode_data=request.form.get('passcode')
        
    #     db.execute(f"SELECT user_pin FROM user WHERE user_name == '{user_data}'") #Getting the user pin from the name of the user
    #     results = db.fetchall()
    
    #     if results[0][0] == passcode_data:
    #         db.execute(f"SELECT user_name FROM user WHERE user_name == '{user_data}'") #Checking to see if the user is in the database and does not have a book out
    #         results = db.fetchall()
    #         if results:
    #             send to library page
    #         else:
    #        
    #                 print("go sign up")

    #           
            
    

    #     def check_out():
    #         db.execute(f"SELECT title FROM book_information WHERE title == '{book_name}' AND book_availability_status == 'Available'") #Using a query to check whether a book exists by seeing if it has data when searched using an SQL query
    #         results = db.fetchall()
    #         if results:
    #             db.execute(f"SELECT id FROM user WHERE user_name == '{user_data}'") #Finding the id of a user whos name has been passed into the function
    #             results = db.fetchall()
    #             user_id = results[0][0]
    #             db.execute(f"UPDATE user SET current_book = '{book_name}', borrowed_date = '{datetime.now()}' WHERE user_name == '{user_data}'") #Checking out the book using an UPDATE query
    #             db.execute(f"UPDATE book_information SET book_availability_status = 'Unavailable', current_user_id = '{user_id}' WHERE title == '{book_name}'")#Updating the books data to match the new user
    #             database.commit()
    #             print(f"You checked out {book_name}!")
    #         else:
    #             print("That book either doesn't exist, or it isn't available right now. Check your spelling.")
    #             database.commit()
            
         
        
    #     return render_template('checkout.html', user=user_data)



    @app.route('/library', methods=['POST', 'GET'])
    def library(): #L:Ibrary function to be called when library.html is loaded
        availability='' #Making all values null when page is loaded
        data=[]
        results=[]
        none=''
        blurb=''
        search_results=''
        if request.method=='POST':
            data=request.form.get("search") #Getting the data from the form called 'search'
            if request.form.get("availability") == None: #If the availability check is checked, change the variable of the database query
                availability=''
            else:
                availability='Availabl'
           
            db.execute(f'''SELECT title, book_availability_status, genre, image_file_path, blurb, book_id FROM book_information JOIN author ON book_information.author_id = author.id WHERE book_availability_status LIKE '{availability}%' AND (author.name = "{data}"  OR genre = "{data}" OR title = "{data}");''') #Doing database query for relevant books after search has been sent

            results=db.fetchall()
            print(results)
            if data == '' and results == []: #Search for everything if the database search had nothing in it
                db.execute(f'''SELECT title, book_availability_status, genre, image_file_path, blurb, book_id, author.name FROM book_information JOIN author ON book_information.author_id = author.id WHERE book_availability_status LIKE '{availability}%';''')
                results=db.fetchall()
            if results:
                none = ''
                search_results='Here are your results!' #Informing user of result status
            else:
                none ='There were no results :('
                search_results=''
                results=''

            
            
        return render_template('library.html', books=results, noresults=none, blurb=blurb, search_results=search_results) #Rendering the library.html template with all of the relevant variable information to be entered in html/css

    @app.route('/book/<int:book_id>') #Sending the book ID key as the name of the page opened, making it unique, and also storing the ID data
    def book(book_id): #Function to find the book information of the book_ID
        db.execute(f'''SELECT title, book_availability_status, genre, image_file_path, blurb, book_id, author.name FROM book_information JOIN author ON book_information.author_id = author.id WHERE book_id = {book_id};''')
        results=db.fetchall()
        print(results)
        return render_template('book_info.html', results=results) #Rendering the page
        
    # @app.route("/checkout/<int:book_id>", method=['POST', 'GET'])
    # def checkout(book_id):
    #     db.execute(f'''SELECT title, book_availability_status, genre, image_file_path, blurb, book_id, author.name FROM book_information JOIN author ON book_information.author_id = author.id WHERE book_id = {book_id};''')
    #     results=db.fetchall()
    #     return render_template('checkout.html', results=results)
    
    @app.route("/login", methods=['POST','GET']) 
    def login():
        user_data=request.form.get('user') #Getting the data entered in the user and passcode forms
        passcode_data=request.form.get('passcode')
        print(user_data,passcode_data)
        db.execute(f"SELECT user_pin FROM user WHERE user_name == '{user_data}'") #Getting the user pin from the name of the user
        results = db.fetchall()
        
        if results:
            print(results[0][0])
            if int(results[0][0]) == int(passcode_data):
                print('hi')
                return redirect(url_for('library')) #If the login data base correct, render the library page
        else:
            print('that person doesnt exist')
            print("go sign up")
            return render_template('login.html') #If the login data is incorrect, render the login page again for retry

    
    @app.route("/about")
    def about():
        return render_template('about.html') #Rendering about.html
    
    @app.route("/events")
    def events():
        return render_template('events.html') #Rendering events.html
    
    @app.route("/contact")
    def contact():
        return render_template('contact.html') #Rendering contact.html

    
    @app.post('/availability')
    def availability_check():
        data=request.form.get("availability") #Getting the status of the availability checkbox

        return redirect("/availability")

if __name__ == '__main__': #Running the programme with debug mode on for better error messages
    app.run(debug=True)