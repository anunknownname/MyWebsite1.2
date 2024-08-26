from flask import Flask, render_template, request, redirect, url_for
import sqlite3
with sqlite3.connect("database.db", check_same_thread=False) as database:
    db=database.cursor()

    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')


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
                availability='Available'
           
            db.execute(f'''SELECT title, book_availability_status, genre, image_file_path, blurb FROM book_information JOIN author ON book_information.author_id = author.id WHERE book_availability_status LIKE '{availability}%' AND (author.name = "{data}"  OR genre = "{data}" OR title = "{data}");''')

            results=db.fetchall()
    
            if results:
                none = ''
                search_results='Here are your results!'
            else:
                none ='There were no results :('
                search_results=''
                results=''
            
            
        return render_template('library.html', books=results, noresults=none, blurb=blurb, search_results=search_results)

    @app.post('/availability')
    def availability_check():
        data=request.form.get("availability")

        return redirect("/availability")




if __name__ == '__main__':
    app.run(debug=True) 