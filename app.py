import json
from flask import Flask, render_template, request, url_for, redirect


app = Flask(__name__)

# Function to read blog posts from the JSON file
def read_jsonfile():
    """Reads blog posts from the data.json file."""
    with open("data.json", "r", encoding="UTF-8") as file:
        return json.load(file)

# Function to write updated blog posts to the JSON file
def write_jsonfile(blog_posts):
    """Writes the updated list of blog posts to the data.json file."""
    with open("data.json", "w", encoding="UTF-8") as file:
        json.dump(blog_posts, file, indent=4)

@app.route('/')
def index():
    """Display the list of blog posts."""
    blog_posts = read_jsonfile()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """Add a new blog post."""
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        blog_posts = read_jsonfile()
        new_id = len(blog_posts) + 1
        new_post = {'id': new_id, 'author': author, 'title': title, 'content': content, 'likes': 0}
        blog_posts.append(new_post)
        write_jsonfile(blog_posts)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """Delete a blog post."""
    blog_posts = read_jsonfile()
    blog_posts = [post for post in blog_posts if post["id"] != post_id]
    write_jsonfile(blog_posts)
    return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Update an existing blog post."""
    blog_posts = read_jsonfile()
    post = next((p for p in blog_posts if p["id"] == post_id), None)

    if not post:
        return redirect(url_for('index'))

    if request.method == 'POST':
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')
        post['likes'] = request.form.get('likes')
        write_jsonfile(blog_posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


# Route to handle "Like" button click
@app.route('/like/<int:id>', methods=['GET'])
def likePost(id):
    blog_posts = read_jsonfile()
    # Find the post with the given id
    post = next((post for post in blog_posts if post['id'] == id), None)

    if post:
        # Increment the 'likes' count
        post['likes'] += 1
    write_jsonfile(blog_posts)
    # Redirect back to the index page
    return redirect(url_for('index'))
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)
