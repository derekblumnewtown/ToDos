# Imports
from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#My app Setup
app = Flask(__name__)

Scss(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False) 
    completed = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Task {self.id}"


with app.app_context():
    db.create_all()

# Routes
# Home page
@app.route('/',methods=['POST','GET'])
def index():

    #Adding tasks to the database
    if request.method == 'POST':
        current_task  = request.form['content']
        new_task = MyTask(content=current_task)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        
        except Exception as e:
            print((f"Error adding task: {e}"))
            return f"Error adding task: {e}"   
   
    #See all current tasks
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template("index.html", tasks=tasks)

#Delete a task
@app.route('/delete/<int:id>')
def delete (id:int):
    task_to_delete = MyTask.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    
    except Exception as e:
        print(f"Error deleting task: {e}")
        return f"Error deleting task: {e}"  



#Update a task
@app.route('/update/<int:id>',methods=['GET','POST'])
def update (id:int):

    task= MyTask.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.add(task)
            db.session.commit()
            return redirect('/')
        
        except Exception as e:
            print(f"Error updating task: {e}")
            return f"Error updating task: {e}"  
    else:
        return render_template("edit.html",task=task)

if __name__ == '__main__':
    app.run(debug=True)