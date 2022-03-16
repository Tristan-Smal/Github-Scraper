from flask import Flask, request, render_template, redirect, Response, url_for
from scraper import *

app = Flask(__name__)

@app.route("/search", methods=["GET","POST"])

def search():   
    search_term = request.args.get("q")
  
    if request.method == "POST":
        if request.form.get("button1"):
            return render_template("template.html", repos = scrape_github(search_term,1)[0:10])
        
        elif request.form.get("button2") == "button2":  
            if search_term == "":
                return render_template("template.html")
            return render_template("template.html", repos = github_api(search_term,1))
    return render_template("template.html")

if __name__ == "__main__":
   app.run(debug = True)