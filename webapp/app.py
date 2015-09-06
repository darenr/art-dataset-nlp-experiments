from flask import Flask, render_template
 
app = Flask(__name__)

@app.route('/')
def homepage():
    title = "Kadist"
    paragraph = ['art work' for x in range(5)] 

    try:
        return render_template("index.html", title = title, paragraph=paragraph)
    except Exception, e:
        return str(e)

if __name__ == "__main__":
  app.run(debug = True, host='0.0.0.0', port=5000, passthrough_errors=True)
