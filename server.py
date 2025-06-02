from flask import Flask, render_template, request
import os
import psycopg2

app = Flask(__name__)

# Connect to your PostgreSQL database using the environment variable from Render
conn = psycopg2.connect(os.environ['DATABASE_URL'])
cur = conn.cursor()

# Create a table (once)
cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id SERIAL PRIMARY KEY,
        email TEXT,
        subject TEXT,
        message TEXT
    );
""")
conn.commit()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.form.to_dict()
        save_to_db(data)  # Save to database instead of CSV
        return render_template('index.html', thank_you=True)
    return render_template('index.html', thank_you=False)

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/components')
def components():
    return render_template('components.html')

def save_to_db(data):
    try:
        cur.execute(
            "INSERT INTO messages (email, subject, message) VALUES (%s, %s, %s)",
            (data.get("email"), data.get("subject"), data.get("message"))
        )
        conn.commit()
    except Exception as e:
        print(f"Database error: {e}")

@app.route('/messages')
def view_messages():
    cur.execute("SELECT email, subject, message FROM messages ORDER BY id DESC")
    rows = cur.fetchall()
    return render_template("messages.html", messages=rows)


if __name__ == '__main__':
    app.run(debug=True)
