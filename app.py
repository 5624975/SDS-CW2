
from flask import Flask, render_template, redirect, url_for, session, flash, request
from config import Config
from models import db, User, Task
from forms import RegistrationForm, LoginForm, TaskForm
#Main App.py
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))
        new_user = User(
            username=form.username.data,
            fullname=form.fullname.data,
            recovery_code=form.recovery_code.data,
            role=form.role.data  # <-- Add this line
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data) and user.recovery_code == form.recovery_code.data:
            session['username'] = user.username
            session['fullname'] = user.fullname
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))

    current_user = User.query.filter_by(username=session['username']).first()
    form = TaskForm()

    # Allow multiple selection of users
    form.assigned_to.choices = [(u.id, u.username) for u in User.query.all()]

    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data
        )
        # Assign multiple users
        selected_user_ids = form.assigned_to.data
        task.assigned_users = User.query.filter(User.id.in_(selected_user_ids)).all()

        db.session.add(task)
        db.session.commit()
        flash('Task created successfully.', 'success')
        return redirect(url_for('dashboard'))

    # Show all tasks if project manager, otherwise only assigned tasks
    if current_user.role == 'manager':
        tasks = Task.query.all()
    else:
        tasks = current_user.assigned_tasks

    users = User.query.all()

    return render_template('dashboard.html', name=current_user.fullname, form=form, users=users, tasks=tasks)

@app.route('/complete_task/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    if 'username' not in session:
        flash('Login required', 'warning')
        return redirect(url_for('login'))

    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed  
    db.session.commit()
    flash('Task completion status updated.', 'info')
    return redirect(url_for('dashboard'))

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if 'username' not in session:
        flash('Login required', 'warning')
        return redirect(url_for('login'))

    task = Task.query.get_or_404(task_id)
    form = TaskForm(obj=task)
    form.assigned_to.choices = [(u.id, u.username) for u in User.query.all()]

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.assigned_to_id = form.assigned_to.data
        db.session.commit()
        flash('Task updated successfully.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_task.html', form=form)

@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    if 'username' not in session:
        flash('Login required', 'warning')
        return redirect(url_for('login'))

    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted.', 'info')
    return redirect(url_for('dashboard'))


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
