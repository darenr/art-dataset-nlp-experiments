from flask import Flask, render_template
 
app = Flask(__name__)

@app.route('/')
def homepage():
    title = "Kadist"
    paragraph = ["wow I am learning so much great stuff!", "wow I am learning so much great stuff!", "wow I am learning so much great stuff!", "wow I am learning so much great stuff!","wow I am learning so much great stuff", "wow I am learning so much great stuff!", "wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!"]

    try:
        return render_template("index.html", title = title, paragraph=paragraph)
    except Exception, e:
        return str(e)

@app.route('/about/contact')
def contactPage():

    title = "About this site"
    paragraph = ["blah blah blah memememememmeme blah blah memememe"]

    pageType = 'about'

    return render_template("index.html", title=title, paragraph=paragraph, pageType=pageType)


 
if __name__ == "__main__":
  app.run(debug = True, host='0.0.0.0', port=5000, passthrough_errors=True)
