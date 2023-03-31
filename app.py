from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:22061998@localhost/testdb'
db=SQLAlchemy(app)

class Todo(db.Model):
    __tablename__='todos'
    id=db.Column(db.Integer, primary_key=True)
    heading=db.Column(db.String(40))
    desc=db.Column(db.String(40))

    def __init__(self, heading, desc):
        self.heading=heading
        self.desc=desc

        


@app.route('/')
def hello():
   allTodo=Todo.query.order_by('id').all()
   return render_template('index.html', data=allTodo)

@app.route('/create_todo', methods=['POST'])
def submit():
   if request.method=='POST':
       heading=request.form['heading']
       desc=request.form['desc']
       todo=Todo(heading, desc)
       db.session.add(todo)
       db.session.commit()
       return redirect('/')
   
@app.route('/delete/<int:id>')
def deleteTodo(id):
    todo=Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>', methods=['GET','POST'])
def updateTodo(id):
       todo=Todo.query.filter_by(id=id).first()
       print(todo.desc)

       if request.method=='GET':
          return render_template('update.html', todo=todo)
       
       elif request.method=='POST':
           heading=request.form['heading']
           desc=request.form['desc']
           todo.heading=heading
           todo.desc=desc
           db.session.commit()
           return redirect('/')

       else:
           return "<h1>not autherised</h1>"
           



    





if __name__=='__main__':
    app.run(debug=True)