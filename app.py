from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os


app = Flask(__name__)


def get_db():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'db'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', 'rootpass'),
        database=os.environ.get('DB_NAME', 'taskdb')
    )


@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        task = request.form['task']
        cursor.execute('INSERT INTO tasks (title) VALUES (%s)', (task,))
        conn.commit()
        return redirect(url_for('index'))
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:task_id>')
def delete(task_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id=%s', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
