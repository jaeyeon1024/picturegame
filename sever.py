from flask import Flask, render_template, request
import Main


app = Flask(__name__)
img , background = Main.create()
Main.reset(background)
@app.route('/')
def index():
    return render_template("index.html" , image_file='css/img/white_background.jpg')


@app.route('/color',methods = ['POST', 'GET'])
def color():
    if request.method == 'POST':
        global background
        result = request.form
        be_rgb = result['rgb']
        rgb = [int(be_rgb[5:],base=16) ,int(be_rgb[3:5],base=16),int(be_rgb[1:3],base=16)]
        Main.print_pexels(img,background,rgb)
        return render_template("index.html" , image_file='css/img/saves.jpg')

app.run(port=5001,debug=True)