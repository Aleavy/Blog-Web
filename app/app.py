from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog_db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    text = db.Column(db.String(800))



@app.route("/")
def hello():
    articles_blog = Blog.query.all()

    return render_template("index.html", articles=articles_blog)

@app.route("/add_article", methods=["POST", "GET"])
def add_article():
    if request.method == "POST":
        title_ar = request.form["title"]
        article = request.form["article"]
        blog_note = Blog(title=title_ar, text=article)
        db.session.add(blog_note)
        db.session.commit()

        return redirect("/")
    else:
        return render_template ("add_an_article.html")
    
@app.route("/delete_article", methods=["POST", "GET"])
def delete_article():
    arts = Blog.query.all()
    id = Blog.query.filter(Blog.id).first()
    if request.method == "POST":
        db.session.delete(id)
        db.session.commit()
        return redirect("/")
    else:
        return render_template("delete_article.html", articles = arts)
    
if __name__ == "__main__":
    app.run(debug=True)
    