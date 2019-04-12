    
from flask import Flask, request, redirect, render_template

app = Flask(__name__)
app.config['DEBUG'] = True

blogs = [] 

@app.route('/newpost', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_title = request.form['blog-title']
        blog_content = request.form['blog-content']
        blogs.append((blog_title, blog_content))

    return render_template('newpost.html',title="Add Blog Entry", blogs=blogs)

@app.route('/', methods=['POST', 'GET'])
def show_blog_posts():
    return render_template('blog.html', title="Show blog Posts", blogs=blogs )
app.run()