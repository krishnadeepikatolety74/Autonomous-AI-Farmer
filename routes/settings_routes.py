from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g, jsonify
from utils.auth import login_required
from models import UserModel, QuickNoteModel, FarmModel

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings', methods=['GET'])
@login_required
def settings():
    user = UserModel.find_by_id(g.user['id'])
    farm = FarmModel.get_by_user_id(user['id'])
    notes = QuickNoteModel.get_all_by_user(user['id'])
    return render_template('settings.html', user=user, farm=farm, notes=notes)


@settings_bp.route('/settings/profile', methods=['POST'])
@login_required
def profile_update():
    user_id = g.user['id']
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()

    if not name:
        flash('Full Name is required.', 'danger')
        return redirect(url_for('settings.settings'))

    if not email:
        flash('Email Address is required.', 'danger')
        return redirect(url_for('settings.settings'))

    # Simple email validation
    if '@' not in email or '.' not in email:
        flash('Please enter a valid email address.', 'danger')
        return redirect(url_for('settings.settings'))

    # Check for duplicate email
    if UserModel.email_exists(email, exclude_user_id=user_id):
        flash('Email Address is already in use by another user.', 'danger')
        return redirect(url_for('settings.settings'))

    UserModel.update_profile(user_id, name, email)
    # Refresh session data
    session['user_email'] = email
    
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('settings.settings'))


@settings_bp.route('/settings/password', methods=['POST'])
@login_required
def password_update():
    user_id = g.user['id']
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')

    user = UserModel.find_by_id(user_id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('settings.settings'))

    # Verify current password
    if not UserModel.verify_password(user['password_hash'], current_password):
        flash('Current password is incorrect.', 'danger')
        return redirect(url_for('settings.settings'))

    if len(new_password) < 8:
        flash('New password must be at least 8 characters long.', 'danger')
        return redirect(url_for('settings.settings'))

    if new_password != confirm_password:
        flash('New passwords do not match.', 'danger')
        return redirect(url_for('settings.settings'))

    UserModel.update_password(user_id, new_password)
    flash('Password updated successfully!', 'success')
    return redirect(url_for('settings.settings'))


@settings_bp.route('/settings/preferences', methods=['POST'])
@login_required
def preferences_update():
    user_id = g.user['id']
    language = request.form.get('language', 'en')
    voice_responses = request.form.get('voice_responses') == 'ON'
    auto_play_voice = request.form.get('auto_play_voice') == 'ON'
    voice = request.form.get('voice', 'Default')

    UserModel.update_preferences(user_id, language, voice_responses, auto_play_voice, voice)
    
    # Translate existing active recommendations to the new language code immediately
    farm = FarmModel.get_by_user_id(user_id)
    if farm:
        try:
            from services.recommendation_service import RecommendationService
            RecommendationService.translate_active_recommendations(farm['id'], language)
        except Exception as e:
            print(f"Failed to translate recommendations: {e}")

    # Sync session preferences
    session['language'] = language
    session['voice_responses'] = voice_responses
    session['auto_play_voice'] = auto_play_voice
    session['voice'] = voice

    flash('Preferences updated successfully!', 'success')
    return redirect(url_for('settings.settings'))


# ── Quick Notes Endpoints ──

@settings_bp.route('/quick-notes', methods=['GET'])
@login_required
def get_quick_notes():
    user_id = g.user['id']
    notes = QuickNoteModel.get_all_by_user(user_id)
    return jsonify({
        "success": True,
        "notes": notes
    })


@settings_bp.route('/quick-notes', methods=['POST'])
@login_required
def create_quick_note():
    user_id = g.user['id']
    farm = FarmModel.get_by_user_id(user_id)
    farm_id = farm['id'] if farm else None

    # Handle both JSON and form data
    if request.is_json:
        data = request.get_json() or {}
        note = data.get('note', '').strip()
    else:
        note = request.form.get('note', '').strip()

    if not note:
        return jsonify({"success": False, "error": "Note content cannot be empty."}), 400

    if len(note) > 200:
        return jsonify({"success": False, "error": "Note exceeds maximum limit of 200 characters."}), 400

    note_id = QuickNoteModel.create(user_id, farm_id, note)
    new_note = QuickNoteModel.get_by_id(note_id, user_id)
    
    return jsonify({
        "success": True,
        "note": new_note
    })


@settings_bp.route('/quick-notes/<int:note_id>/complete', methods=['POST'])
@login_required
def complete_quick_note(note_id):
    user_id = g.user['id']
    
    # Check ownership
    note = QuickNoteModel.get_by_id(note_id, user_id)
    if not note:
        return jsonify({"success": False, "error": "Note not found or access denied."}), 404

    # Toggle completeness
    if request.is_json:
        data = request.get_json() or {}
        completed = data.get('completed', 1)
    else:
        # If no body specified, default to completed=1
        completed = 1

    QuickNoteModel.complete(note_id, user_id, completed)
    updated_note = QuickNoteModel.get_by_id(note_id, user_id)
    
    return jsonify({
        "success": True,
        "note": updated_note
    })


@settings_bp.route('/quick-notes/<int:note_id>', methods=['DELETE'])
@login_required
def delete_quick_note(note_id):
    user_id = g.user['id']
    
    note = QuickNoteModel.get_by_id(note_id, user_id)
    if not note:
        return jsonify({"success": False, "error": "Note not found or access denied."}), 404

    QuickNoteModel.delete(note_id, user_id)
    return jsonify({
        "success": True,
        "message": "Note deleted successfully."
    })


@settings_bp.route('/quick-notes/clear-completed', methods=['POST'])
@login_required
def clear_completed_notes():
    user_id = g.user['id']
    QuickNoteModel.clear_completed(user_id)
    return jsonify({
        "success": True,
        "message": "Completed notes cleared successfully."
    })
