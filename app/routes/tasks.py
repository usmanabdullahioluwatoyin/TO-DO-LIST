from flask import Blueprint, render_template, redirect, session, request, flash, abort, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.helpers.model import User, Task
from app.forms.task_forms import TaskForm, UpdateTaskForm
tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/', methods=['GET', 'POST'])
@login_required
def user_dashboard():

    task_filter = request.args.get('filter', 'all').lower()
    query = Task.query.filter_by(user_id=current_user.id)

    if task_filter == 'active':
        query = query.filter(Task.is_complete == False)

    elif task_filter == 'completed':
        query = query.filter(Task.is_complete == True)

    tasks = query.order_by(
        Task.is_complete.asc(),
        Task.due_date.asc(),
        Task.created_at.desc()
    ).all()

    return render_template('dashboard.html', tasks=tasks, task_filter=task_filter)

@tasks_bp.route('/create-task', methods=['GET', 'POST'])
@login_required
def create():
    task = TaskForm()

    if task.validate_on_submit():
        new_task = Task(
            title = task.title.data.strip(),
            description = task.description.data.strip(),
            due_date = task.due_date.data,
            user_id = current_user.id

        )
        db.session.add(new_task)
        db.session.commit()

        flash("New Task created", "success")
        return redirect(url_for('tasks.user_dashboard'))

    return render_template('task-form.html', task=task)
@tasks_bp.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)

    task_edit = UpdateTaskForm(obj=task) 
    if task_edit.validate_on_submit():
        task_edit.populate_obj(task) 
        db.session.commit()
        flash("Task updated successfully", "success")
        return redirect(url_for('tasks.user_dashboard'))

    return render_template('edit-task.html', task_edit=task_edit, task=task)

@tasks_bp.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):


    task = Task.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        abort(403)

    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully", "success")

    return redirect(url_for('tasks.user_dashboard', task=task))

        
@tasks_bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
@login_required
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        abort(403)
    
    task.is_complete = not task.is_complete

    db.session.commit()

    return redirect(url_for('tasks.user_dashboard', task=task))

        


