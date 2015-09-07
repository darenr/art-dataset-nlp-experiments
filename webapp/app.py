from flask import Flask, render_template
 
app = Flask(__name__)

@app.route('/')
def homepage():
    title = "Kadist"
    results = [{"title": "bronze sculpture", "description": "bla bla bla"}]

    try:
        return render_template("index.html", title = title, results=results)
    except Exception, e:
        return str(e)

if __name__ == "__main__":
  app.run(debug = True, host='0.0.0.0', port=5000, passthrough_errors=True)
