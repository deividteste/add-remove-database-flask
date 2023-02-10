from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '1234'

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

class User(db.Model):
    __tablename_ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    age = db.Column(db.Integer)

class UserCreation(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    age = IntegerField("Age: ", validators=[DataRequired()])
    submit2 = SubmitField("Submit")

class UserDelete(FlaskForm):
    name = StringField("Name:", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/', methods=['GET', 'POST'])
def index():
    users = User.query.all()
    add_form = UserCreation()
    remove_form = UserDelete()

    if add_form.validate_on_submit():
        print("Chegou aqui!")
        user = User(name=add_form.name.data, age=add_form.age.data)
        
        db.session.add(user)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash("Não é possível adicionar um usuário que já existe.", "error")
        else:
            flash("Usuário adicionado com sucesso!", "success")
        
        return redirect(url_for('index'))

    if remove_form.validate_on_submit():
        user = User.query.filter_by(name=remove_form.name.data).first()

        if user == None:
            remove_form.name.data = ''
            flash("Não existe usuário com esse nome.", "error")

            return redirect(url_for('index'))

        else:
            db.session.delete(user)
            db.session.commit()

            flash('Usuário removido com sucesso.', "warning")

            return redirect(url_for('index'))

    return render_template("index.html", users=users, add_form=add_form, remove_form=remove_form)

if __name__ == "__main__":
    app.run(debug=True)