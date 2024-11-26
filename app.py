import json

from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect

app = Flask(__name__)
def read_jsonfile():
    with open("data.json", "r") as fileobj:
        blog_posts = json.load(fileobj)
        return blog_posts

# Function to write the updated list of blog posts to the JSON file
def write_jsonfile(blog_posts):
    with open("data.json", "w") as fileobj:
        json.dump(blog_posts, fileobj, indent=4)


@app.route('/')
def index():
     blog_posts = read_jsonfile()
     print(blog_posts)
     return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        blog_posts = read_jsonfile()
        # Generate a new ID for the new post (you can improve this by using a unique ID generator or database)
        new_id = len(blog_posts) + 1

        # Create a new blog post and append to the blog_posts list
        new_post = {'id': new_id, 'author': author, 'title': title, 'content': content}
        blog_posts.append(new_post)
        write_jsonfile(blog_posts)
        return redirect(url_for('index'))
    return render_template('add.html')
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)