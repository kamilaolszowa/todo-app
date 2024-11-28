from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    complete = db.Column(db.Boolean)


with app.app_context():
    db.create_all()

    new_todo = Todo(title="todo 1", complete=False)
    # db.session.add(new_todo)
    # db.session.commit()


@app.route('/')
def index():
    todo_list = Todo.query.all()
    print(todo_list)
    return render_template('base.html', todo_list=todo_list)


@app.route('/about')
def about():
    return "About"


if __name__ == "__main__":
    app.run(debug=True)
