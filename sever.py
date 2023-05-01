from flask import Flask, render_template, request
import Main.py

app = Flask(__name__)
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return Main() [int(result[0]),int(result[1]),int(result[2])]




app.run(port=5001,debug=True)