from flask import Flask, render_template, request, redirect
import sqlite3
with sqlite3.connect("database.db", check_same_thread=False) as database:
    db=database.cursor()

    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')


    @app.route('/library', methods=['POST', 'GET'])
    def library_author():
        data=[]
        results=''
        none=''
        blurb=''
        if request.method=='POST':
            data=request.form.get("search")
            db.execute(f'''SELECT title, book_availability_status, genre FROM book_information JOIN author ON book_information.author_id = author.id WHERE author.name == ?;''', (data,))
            results=db.fetchall()
            print(results[0])
            if results:
                none = ''
                search_results='Here are your results!'
            else:
                none ='There were no results :('
                search_results=''
            db.execute(f'SELECT blurb, size FROM book_information JOIN author ON book_information.author_id = author_id WHERE author.name == ?;', (data,))
            blurb=db.fetchall()
        return render_template('library.html', books=results, noresults=none, blurb=blurb, search_results=search_results)

    @app.post('/search')
    def search():
        data=request.form.get("search")
        print(data)
        return redirect('/search')





if __name__ == '__main__':
    app.run(debug=True) 