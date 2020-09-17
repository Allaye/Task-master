"""app.py"""
# pylint: disable=missing-docstring,too-few-public-methods,invalid-name

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
    
        task_content = request.form.get('content')
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task) 
            db.session.commit()
            return redirect('/')

        except:
            return "There is an error adding task"
            
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()

        return render_template('index.html', tasks=tasks) 


@app.route("/delete/<int:id>")
def delete_task(id):
    task_to_be_deleted = Todo.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_be_deleted)
        db.session.commit()
        return redirect('/')

    except:
        return "Error deleting the selected task..."

@app.route('/update/<int:id>', methods=["POST", "GET"])
def update_task(id):
    task = Todo.query.get_or_404(id)

    if request.method == "POST":
        task.content = request.form.get('content')

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Error whiles trying to update your task"

    else:
        return render_template('/update.html', task=task)





if __name__ == "__main__": 

    app.run(debug=True)