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
        results=''
        none=''
        blurb=''
        search_results=''
        if request.method=='POST':
            data=request.form.get("search")
            availability=request.form.getlist("availability")
            print(availability)
            db.execute(f'''SELECT title, book_availability_status, genre, image_file_path FROM book_information JOIN author ON book_information.author_id = author.id WHERE author.name == ?;''', (data,))
            results=db.fetchall()
            if results:
                none = ''
                search_results='Here are your results!'
            else:
                none ='There were no results :('
                search_results=''
            db.execute(f'SELECT blurb, size FROM book_information JOIN author ON book_information.author_id = author_id WHERE author.name == ?;', (data,))
            blurb=db.fetchall()
        return render_template('library.html', books=results, noresults=none, blurb=blurb, search_results=search_results)

    @app.post('/availability')
    def availability_check():
        data=request.form.get("availability")

        return redirect("/availability")




if __name__ == '__main__':
    app.run(debug=True) 