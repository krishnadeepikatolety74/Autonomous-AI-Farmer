from flask import Blueprint, render_template, send_file, g, flash, redirect, url_for
from utils.auth import login_required
from models import FarmModel, CropModel, ObservationModel, RecommendationModel, AlertModel, AgentRunModel, MemoryModel
from services.report_service import ReportService
import json

report_bp = Blueprint('report', __name__)

@report_bp.route('/report')
@login_required
def report():
    user = g.user
    farm = FarmModel.get_by_user_id(user['id'])
    crop = CropModel.get_by_farm_id(farm['id']) if farm else None
    observation = ObservationModel.get_latest(farm['id']) if farm else None
    recommendations = RecommendationModel.get_active(farm['id']) if farm else []
    alerts = AlertModel.get_unread_by_farm(farm['id']) if farm else []
    recent_runs = AgentRunModel.get_recent(farm['id'], limit=7) if farm else []

    # Try to extract final plan from latest Farm Planning Agent run
    final_plan = None
    if farm:
        planning_runs = AgentRunModel.get_by_agent(farm['id'], 'Farm Planning Agent')
        if planning_runs:
            try:
                output = planning_runs[0].get('output_json', '{}')
                final_plan = json.loads(output) if isinstance(output, str) else output
            except (json.JSONDecodeError, TypeError):
                final_plan = None

    return render_template('report.html',
        user=user, farm=farm, crop=crop,
        observation=observation,
        recommendations=recommendations,
        alerts=alerts,
        recent_runs=recent_runs,
        final_plan=final_plan
    )

@report_bp.route('/report/generate', methods=['POST'])
@login_required
def generate_report():
    user = g.user
    farm = FarmModel.get_by_user_id(user['id'])
    if not farm:
        flash('Please set up your farm profile first.', 'error')
        return redirect(url_for('report.report'))

    crop = CropModel.get_by_farm_id(farm['id'])
    observation = ObservationModel.get_latest(farm['id'])
    recommendations = RecommendationModel.get_active(farm['id'])
    alerts = AlertModel.get_unread_by_farm(farm['id'])
    recent_runs = AgentRunModel.get_recent(farm['id'], limit=7)

    # Extract final plan
    final_plan = None
    planning_runs = AgentRunModel.get_by_agent(farm['id'], 'Farm Planning Agent')
    if planning_runs:
        try:
            output = planning_runs[0].get('output_json', '{}')
            final_plan = json.loads(output) if isinstance(output, str) else output
        except (json.JSONDecodeError, TypeError):
            final_plan = None

    # Convert sqlite3.Row objects to dicts
    farm_dict = dict(farm) if farm else {}
    crop_dict = dict(crop) if crop else {}
    obs_dict = dict(observation) if observation else {}
    rec_list = [dict(r) for r in recommendations] if recommendations else []
    alert_list = [dict(a) for a in alerts] if alerts else []
    run_list = [dict(r) for r in recent_runs] if recent_runs else []

    pdf_buffer = ReportService.generate_pdf(
        farm=farm_dict,
        crop=crop_dict,
        observation=obs_dict,
        recommendations=rec_list,
        alerts=alert_list,
        recent_runs=run_list,
        final_plan=final_plan
    )

    farm_name = farm_dict.get('name', 'Farm').replace(' ', '_')
    filename = f"AI_Farm_Report_{farm_name}.pdf"

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf'
    )
