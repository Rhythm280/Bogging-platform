from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Initialize the database
def init_db():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS posts (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT,
                 content TEXT,
                 date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

# Home Route
@app.route('/')
def home():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts ORDER BY date DESC")
    posts = c.fetchall()
    conn.close()
    return render_template('home.html', posts=posts)

# Create Post Route
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        if not title or not content:
            flash("Title and Content are required!", "error")
        else:
            conn = sqlite3.connect('blog.db')
            c = conn.cursor()
            c.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('home'))
    return render_template('create.html')

# Edit Post Route
@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = c.fetchone()
    conn.close()
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = sqlite3.connect('blog.db')
        c = conn.cursor()
        c.execute("UPDATE posts SET title = ?, content = ? WHERE id = ?", (title, content, post_id))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    
    return render_template('edit.html', post=post)

# Delete Post Route
@app.route('/delete/<int:post_id>')
def delete(post_id):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    # Initialize the database before running the app
    init_db()
    app.run(debug=True)
