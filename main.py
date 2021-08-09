from flask import *
import sqlite3
from datetime import *
import json
import cryptocode

app = Flask(__name__)
app.secret_key = '1a2b3c4d5e'
import sys


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/usersignup", methods=["POST"])
def usersignup():
    if request.method == "POST":
        try:
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
            # d_password=cryptocode.decrypt(password,"blogpassword")
            with sqlite3.connect("blog.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO user(username, email, password) values(?,?,?)", (username, email, password))
                flash("Successfully created", "success")
                # flash("Successfully Created")
            # print(password)
            # print(d_password)
            # print(request.form)
            # sys.exit()
        except:
            con.rollback()
            flash("Error in updation", "danger")

        finally:
            return render_template("index.html")


@app.route("/usersignin", methods=["POST"])
def usersignin():
    if request.method == "POST":
        # print(request.form)
        # sys.exit()
        # try:
        username = request.form["username"]
        # email = request.form["email"]
        password = request.form["password"]
        # print(password)
        # sys.exit()
        with sqlite3.connect("blog.db") as con:
            cur = con.cursor()
            cur.execute('SELECT * FROM user WHERE username = ? AND password = ?', (username, password))
            result = cur.fetchone()
            if result:
                author = result[0]
                with sqlite3.connect("blog.db") as con:
                    con.row_factory = sqlite3.Row
                    cur = con.cursor()
                    blog_list = cur.execute(
                        '''SELECT b.id, b.name, b.content,b.author,count(c.comment) as totalcomments from blog as b LEFT JOIN comment as c on b.id = c.blog WHERE author=? group by b.id ''',
                        [session['id']]).fetchall()
                    all_blog_list = cur.execute(
                        '''SELECT b.id, b.name, b.content,b.author,count(c.comment) as totalcomments from blog as b LEFT JOIN comment as c on b.id = c.blog  WHERE author!=? group by b.id''',
                        [session['id']]).fetchall()
                    session['loggedin'] = True
                    session['id'] = result[0]
                    session['username'] = result[1]
                    session['email'] = result[2]
                    flash("Successfully logged in", "success")
                    return render_template("home.html", bloglist=blog_list, all_blogs=all_blog_list)
            else:
                flash("Incorrect username or password", "danger")
                return render_template("index.html")


@app.route("/createblog")
def createblog():
    return render_template("createblog.html")


@app.route("/postblog", methods=["POST"])
def postblog():
    if request.method == "POST":
        name = request.form["title"]
        content = request.form["content"]
        author = session['id']
        created_date = datetime.now()
        modified_date = datetime.now()
        with sqlite3.connect("blog.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO blog(name, content,author,created_date,modified_date) values(?,?,?,?,?)",
                        (name, content, author, created_date, modified_date))
            flash("Successfully posted", "success")
            with sqlite3.connect("blog.db") as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                # blog_list = cur.execute('''SELECT * FROM blog WHERE author=?''', [session['id']]).fetchall()
                blog_list = cur.execute(
                    '''SELECT b.id, b.name, b.content,b.author,count(c.comment) as totalcomments from blog as b LEFT JOIN comment as c on b.id = c.blog WHERE author=? group by b.id ''',
                    [session['id']]).fetchall()
                return render_template("home.html", bloglist=blog_list)


@app.route("/readblog/<id>")
def readblog(id=0):
    with sqlite3.connect("blog.db") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        view_blog = cur.execute('''SELECT * FROM blog WHERE id=?''', id).fetchone()
        return render_template("viewblog.html", content=view_blog)


@app.route("/commentblog/<id>")
def commentblog(id=0):
    return render_template("comment.html", id=id)


@app.route("/comment", methods=["POST"])
def comment():
    if request.method == "POST":
        # print(request.form)
        # sys.exit()
        comment = request.form["comment"]
        blogid = request.form["blogid"]

        userid = session['id']
        created_date = datetime.now()
        modified_date = datetime.now()
        with sqlite3.connect("blog.db") as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("INSERT INTO comment(blog, user,comment,created_date,modified_date) values(?,?,?,?,?)",
                        (blogid, userid, comment, created_date, modified_date))
            blog_info = cur.execute(
                '''SELECT b.id, b.name, b.content,b.author,count(c.comment) as totalcomments from blog as b LEFT JOIN comment as c on b.id = c.blog WHERE author=? group by b.id ''',
                [session['id']]).fetchall()

            all_blog_info = cur.execute(
                '''SELECT b.id, b.name, b.content,b.author,count(c.comment) as totalcomments from blog as b LEFT JOIN comment as c on b.id = c.blog  WHERE author!=? group by b.id''',
                [session['id']]).fetchall()

            return render_template("home.html", bloglist=blog_info, all_blogs=all_blog_info)

@app.route("/like_or_dislike", methods=["POST"])
def like_or_dislike():
    if request.method=="POST":
        blog_id=request.form["id"]
        action=request.form["action"]
        user=session['id']
        action_date=datetime.now()
        with sqlite3.connect("blog.db") as con:
            # con.row_factory = sqlite3.Row
            cur = con.cursor()
            a=1
            b=0
            if action=="like":
                cur.execute("INSERT INTO response(blog, user,like_or_not,response_date) values(?,?,?,?)",
                            (blog_id,user,1,action_date))
                count=cur.execute('''SELECT count(like_or_not) as like_dislike_count FROM response WHERE like_or_not=? AND blog=?''',[a],[blog_id]).fetchall()
                # print(count)
            else:
                cur.execute("INSERT INTO response(blog, user,like_or_not, response_date) values(?,?,?,?)",
                            (blog_id,user,0,action_date))
                count=cur.execute('''SELECT count(like_or_not) as like_dislike_count FROM response WHERE like_or_not=? AND blog=?''',[b], [blog_id]).fetchall()
                # print(count)
        # for c in count:
        #     print(str(c))
        # count_str=str(count)
        return jsonify(count=count)
        # sys.exit()


if __name__ == "__main__":
    app.run(debug=True)
