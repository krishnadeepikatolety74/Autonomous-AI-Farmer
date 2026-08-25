from flask import Blueprint, render_template, redirect, url_for, flash, g, jsonify
from utils.auth import login_required
from models import FarmModel, AlertModel

alert_bp = Blueprint('alerts', __name__)

@alert_bp.route('/alerts')
@login_required
def alerts():
    user = g.user
    farm = FarmModel.get_by_user_id(user['id'])
    all_alerts = []
    if farm:
        all_alerts = AlertModel.get_all_by_farm(farm['id'])
    return render_template('alerts.html', user=user, farm=farm, alerts=all_alerts)

@alert_bp.route('/alerts/<int:alert_id>/read', methods=['POST'])
@login_required
def mark_read(alert_id):
    user = g.user
    alert = AlertModel.get_by_id_and_user(alert_id, user['id'])
    if not alert:
        flash('Alert not found.', 'error')
        return redirect(url_for('alerts.alerts'))
    AlertModel.mark_as_read(alert_id, alert['farm_id'])
    flash('Alert marked as read.', 'success')
    return redirect(url_for('alerts.alerts'))

@alert_bp.route('/alerts/<int:alert_id>/dismiss', methods=['POST'])
@login_required
def dismiss(alert_id):
    user = g.user
    alert = AlertModel.get_by_id_and_user(alert_id, user['id'])
    if not alert:
        flash('Alert not found.', 'error')
        return redirect(url_for('alerts.alerts'))
    AlertModel.dismiss(alert_id, alert['farm_id'])
    flash('Alert dismissed.', 'success')
    return redirect(url_for('alerts.alerts'))
