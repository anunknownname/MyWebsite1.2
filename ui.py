from flask import Flask, render_template, request, redirect
import sqlite3
with sqlite3.connect("database.db", check_same_thread=False) as database:
    db=database.cursor()

    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')


    @app.route('/library', methods=['POST', 'GET'])
    def library():
        data=[]
        results=''
        none=''
        if request.method=='POST':
            data=request.form.get("search")
            db.execute(f'''SELECT book_information.id, title, size, book_availability_status, blurb, genre FROM book_information JOIN author ON book_information.author_id = author.id WHERE author.name == ?;''', (data,))
            results=db.fetchall()
            print(results)
            if results:
                none = ''
            else:
                none ='there were no results'
        return render_template('library.html', books=results, noresults=none)

    @app.post('/search')
    def search():
        data=request.form.get("search")
        print(data)
        return redirect('/search')





if __name__ == '__main__':
    app.run(debug=True) 