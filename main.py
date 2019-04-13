    
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Shooter1$@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120)) 
    body = db.Column(db.String(500))
    deleted = db.Column(db.Boolean, default=False)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.completed = False



@app.route('/newpost', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_title = request.form['blog-title']
        blog_body = request.form['blog-body']
        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.all()
    

    #this should redirect to ?!!!
    #return redirect('/')
    return render_template('newpost.html',title="Add Blog Entry", blogs=blogs)
    

@app.route('/', methods=['POST', 'GET'])
def show_blog_posts():
    blogs = Blog.query.all()
    return render_template('blog.html', title="Show blog Posts", blogs=blogs )

#delete blog posts
@app.route('/delete-post', methods=['POST'])
def delete_post():
    blog_id = int(request.form['blog-id'])
    blog = Blog.query.get(blog_id)
    db.session.delete(blog)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run()