from flask import Blueprint, render_template, redirect, url_for, flash, g
from utils.auth import login_required
from models import FarmModel, RecommendationModel

recommendation_bp = Blueprint('recommendations', __name__)

@recommendation_bp.route('/recommendations')
@login_required
def recommendations_list():
    user = g.user
    farm = FarmModel.get_by_user_id(user['id'])
    recs = RecommendationModel.get_all(farm['id']) if farm else []

    return render_template('recommendations.html', user=user, farm=farm, recommendations=recs)

@recommendation_bp.route('/recommendations/<int:rec_id>/complete', methods=['POST'])
@login_required
def mark_complete(rec_id):
    user = g.user
    farm = FarmModel.get_by_user_id(user['id'])
    if farm:
        RecommendationModel.mark_completed(rec_id, farm['id'])
        flash('Recommendation marked as completed!', 'success')
    return redirect(url_for('recommendations.recommendations_list'))
