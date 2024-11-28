from flask import Flask, render_template, request, redirect, url_for
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


def redirect_to_index(error=None):
    return redirect(url_for("index", error=error))


@app.route('/')
def index():
    todo_list = Todo.query.all()
    error = request.args.get('error')
    return render_template('base.html', todo_list=todo_list, error=error)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    if not title or not title.strip():
        return redirect_to_index(error="Title is required")
    if len(title) > 255:
        return redirect_to_index(error="Title is too long")
    try:
        new_todo = Todo(title=title, complete=False)
        db.session.add(new_todo)
        db.session.commit()
    except Exception as e:
        return redirect_to_index(error=f'Error adding todo: {e}')
    return redirect_to_index()


@app.route("/update/<int:todo_id>")
def update(todo_id):
    try:
        todo = Todo.query.filter_by(id=todo_id).first()
        if todo:
            todo.complete = not todo.complete
            db.session.commit()
        else:
            return redirect_to_index(error="Todo not found")
    except Exception as e:
        return redirect_to_index(error=f"Error updating todo: {e}")
    return redirect_to_index()


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    try:
        todo = Todo.query.filter_by(id=todo_id).first()
        if todo:
            db.session.delete(todo)
            db.session.commit()
        else:
            return redirect_to_index(error="Todo not found")
    except Exception as e:
        return redirect_to_index(error=f"Error deleting todo: {e}")
    return redirect_to_index()


@app.route('/about')
def about():
    return "About"


if __name__ == "__main__":
    app.run(debug=True)
