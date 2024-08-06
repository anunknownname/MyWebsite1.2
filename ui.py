from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/library')
def library():
    return render_template('library.html')

@app.post('/search')
def search():
    data=request.form.get("search")
    print(data)
    return redirect('/library')





if __name__ == '__main__':
    app.run(debug=True) 