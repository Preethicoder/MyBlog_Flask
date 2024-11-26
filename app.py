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

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    blog_posts = read_jsonfile()
    for post in blog_posts:
        if post["id"] == post_id:
            blog_posts.remove(post)
            break
    write_jsonfile(blog_posts)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    blog_posts = read_jsonfile()  # Read the blog posts from the JSON file

    # Initialize post variable to None
    post = None

    # Find the post by matching the id
    for p in blog_posts:
        if p["id"] == post_id:
            post = p
            break  # Stop searching once we find the post

    # If the post is not found, redirect to the home page
    if not post:
        return redirect(url_for('index'))

    # If it's a POST request, update the post
    if request.method == 'POST':
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')

        write_jsonfile(blog_posts)  # Save the updated blog posts back to the file
        return redirect(url_for('index'))  # Redirect to the index page after updating

    # If it's a GET request, display the update form with current post details
    return render_template('update.html', post=post)  # Render the update template with the post data



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)