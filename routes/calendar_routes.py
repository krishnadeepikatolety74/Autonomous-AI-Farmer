from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from utils.auth import login_required
from models import FarmModel, TaskModel

calendar_bp = Blueprint('calendar', __name__)

@calendar_bp.route('/calendar')
@login_required
def calendar():
    user = g.user
    farm = FarmModel.get_by_user_id(user['id'])
    tasks = TaskModel.get_all_by_user(user['id'])
    return render_template('calendar.html', user=user, farm=farm, tasks=tasks)

@calendar_bp.route('/calendar', methods=['POST'])
@login_required
def create_task():
    user = g.user
    farm = FarmModel.get_by_user_id(user['id'])
    farm_id = farm['id'] if farm else None

    task_name = request.form.get('task_name', '').strip()
    task_type = request.form.get('task_type', 'Other').strip()
    due_date = request.form.get('due_date', '').strip()

    if not task_name or not due_date:
        flash('Task name and due date are required.', 'error')
        return redirect(url_for('calendar.calendar'))

    TaskModel.create(user['id'], farm_id, task_name, task_type, due_date)
    flash('Task added successfully!', 'success')
    return redirect(url_for('calendar.calendar'))

@calendar_bp.route('/calendar/<int:task_id>/complete', methods=['POST'])
@login_required
def complete_task(task_id):
    user = g.user
    task = TaskModel.get_by_id(task_id, user['id'])
    if not task:
        flash('Task not found.', 'error')
        return redirect(url_for('calendar.calendar'))
    new_status = 0 if task['completed'] else 1
    TaskModel.complete(task_id, user['id'], new_status)
    flash('Task status updated.', 'success')
    return redirect(url_for('calendar.calendar'))

@calendar_bp.route('/calendar/<int:task_id>', methods=['DELETE', 'POST'])
@login_required
def delete_task(task_id):
    user = g.user
    # Support both DELETE method and POST with _method=DELETE
    if request.method == 'POST' and request.form.get('_method') != 'DELETE':
        # This is actually the complete toggle from above, redirect
        return redirect(url_for('calendar.calendar'))
    
    task = TaskModel.get_by_id(task_id, user['id'])
    if not task:
        if request.is_json:
            return jsonify({'success': False, 'message': 'Task not found.'}), 404
        flash('Task not found.', 'error')
        return redirect(url_for('calendar.calendar'))
    
    TaskModel.delete(task_id, user['id'])
    if request.is_json:
        return jsonify({'success': True, 'message': 'Task deleted.'})
    flash('Task deleted.', 'success')
    return redirect(url_for('calendar.calendar'))
