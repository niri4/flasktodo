from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

class ToDo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(200), nullable=False)
  completed = db.Column(db.Integer, default=0)
  date_created = db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self):
    return '<Task %r>' % self.id
with app.app_context():
  db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
  if request.method == 'POST':
    task_content = request.form['content']
    new_task = ToDo(content=task_content)

    try:
      db.session.add(new_task)
      db.session.commit()
      return redirect("/")
    except:
      return 'There was an issue adding your task'
  else:
    tasks = ToDo.query.order_by(ToDo.date_created).all()
    return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
  try:
    db.session.delete(__task(id))
    db.session.commit()
    return redirect("/")
  except:
    return "There was an issue deleting your task"

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
  task = __task(id)
  if request.method == 'POST':
    task.content = request.form['content'] 
    try:
      db.session.commit()
      return redirect("/")
    except:
      return "There was an issue deleting your task"
  else:
    return render_template('update.html', task=task)

def __task(id):
  return ToDo.query.get_or_404(id)

if __name__ == "__main__":
  app.run(debug=True)