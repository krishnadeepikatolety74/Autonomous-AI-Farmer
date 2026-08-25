from flask import Blueprint, render_template, g
from utils.auth import login_required
from models import FarmModel, MemoryModel

memory_bp = Blueprint('memory', __name__)

@memory_bp.route('/memory')
@login_required
def memory_list():
    user = g.user
    farm = FarmModel.get_by_user_id(user['id'])
    memories = MemoryModel.get_recent(farm['id'], limit=20) if farm else []

    return render_template('memory.html', user=user, farm=farm, memories=memories)

@memory_bp.route('/activity')
@login_required
def activity_list():
    from models import AgentRunModel
    user = g.user
    farm = FarmModel.get_by_user_id(user['id'])
    runs = AgentRunModel.get_all(farm['id'], limit=50) if farm else []

    return render_template('activity.html', user=user, farm=farm, runs=runs)
