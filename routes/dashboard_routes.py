import json
from flask import Blueprint, render_template, session, g
from utils.auth import login_required
from models import FarmModel, CropModel, ObservationModel, AgentRunModel, RecommendationModel, QuickNoteModel

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/overview')
@login_required
def overview():
    user = g.user
    farm = FarmModel.get_by_user_id(user['id']) if user else None
    crop = CropModel.get_by_farm_id(farm['id']) if farm else None
    observation = ObservationModel.get_latest(farm['id']) if farm else None
    recommendations = RecommendationModel.get_active(farm['id']) if farm else []
    
    # Get latest agent run statuses
    agent_names = ['Weather Agent', 'Soil Agent', 'Crop Disease Agent',
                   'Market Agent', 'Irrigation Agent', 'Fertilizer Agent', 'Farm Planning Agent']
    agent_statuses = {}
    if farm:
        for name in agent_names:
            run = AgentRunModel.get_latest_by_agent(farm['id'], name)
            agent_statuses[name] = run

    return render_template('overview.html',
        user=user,
        farm=farm,
        crop=crop,
        observation=observation,
        recommendations=recommendations,
        agent_statuses=agent_statuses
    )

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    user = g.user
    farm = FarmModel.get_by_user_id(user['id']) if user else None
    crop = CropModel.get_by_farm_id(farm['id']) if farm else None
    observation = ObservationModel.get_latest(farm['id']) if farm else None
    recent_runs = AgentRunModel.get_all(farm['id'], limit=10) if farm else []
    recommendations = RecommendationModel.get_active(farm['id']) if farm else []
    
    # Fetch incomplete quick notes for the dashboard widget
    incomplete_notes = QuickNoteModel.get_incomplete_by_user(user['id'], limit=5)

    # Parse output_json for each run
    for run in recent_runs:
        if run.get('output_json'):
            try:
                run['parsed_output'] = json.loads(run['output_json'])
            except:
                run['parsed_output'] = {}

    return render_template('dashboard.html',
        user=user,
        farm=farm,
        crop=crop,
        observation=observation,
        recent_runs=recent_runs,
        recommendations=recommendations,
        incomplete_notes=incomplete_notes
    )

@dashboard_bp.route('/trends')
@login_required
def trends():
    user = g.user
    farm = FarmModel.get_by_user_id(user['id']) if user else None
    
    observations = []
    if farm:
        # Get up to 20 historical readings, reverse to make them chronological
        raw_obs = ObservationModel.get_all(farm['id'], limit=20)
        observations = list(reversed(raw_obs))

    return render_template('trends.html',
        user=user,
        farm=farm,
        observations=observations
    )

