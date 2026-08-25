import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from utils.auth import login_required
from models import FarmModel, CropModel, ObservationModel, AgentRunModel
from services.agent_orchestrator import AgentOrchestrator
from services.language_service import LanguageService

agent_bp = Blueprint('agents', __name__)

# Agent metadata for rendering cards
AGENT_META = {
    'Weather Agent': {
        'slug': 'weather',
        'emoji': '🌦️',
        'icon': 'agent-weather.png',
        'description': 'Monitors local weather and climate conditions to predict crop-climate risks.',
        'color': '#8CC8F2'
    },
    'Soil Agent': {
        'slug': 'soil',
        'emoji': '🌱',
        'icon': 'agent-soil.png',
        'description': 'Analyzes soil health, hydration, and nutrient (N-P-K) levels.',
        'color': '#6FAF7B'
    },
    'Crop Disease Agent': {
        'slug': 'crop-disease',
        'emoji': '🌾',
        'icon': 'agent-crop-disease.png',
        'description': 'Monitors crop health and detects diseases early.',
        'color': '#D97D7D'
    },
    'Irrigation Agent': {
        'slug': 'irrigation',
        'emoji': '💧',
        'icon': 'agent-irrigation.png',
        'description': 'Optimizes water distribution and valve schedules.',
        'color': '#59B8E8'
    },
    'Fertilizer Agent': {
        'slug': 'fertilizer',
        'emoji': '🧪',
        'icon': 'agent-fertilizer.png',
        'description': 'Generates crop-specific nutrient application plans.',
        'color': '#E8B85C'
    },
    'Market Agent': {
        'slug': 'market',
        'emoji': '📈',
        'icon': 'agent-market.png',
        'description': 'Tracks commodity prices and optimal selling windows.',
        'color': '#B38CD9'
    },
    'Farm Planning Agent': {
        'slug': 'farm-planning',
        'emoji': '🧠',
        'icon': 'agent-farm-planning.png',
        'description': 'Coordinates data from all agents to synthesize one unified strategy.',
        'color': '#285943'
    }
}


def _slug_to_name(slug):
    """Convert URL slug to agent display name."""
    for name, meta in AGENT_META.items():
        if meta['slug'] == slug:
            return name
    return None


@agent_bp.route('/agents')
@login_required
def agents_list():
    user = g.user
    farm = FarmModel.get_by_user_id(user['id'])

    agents_data = []
    for name, meta in AGENT_META.items():
        agent_info = dict(meta)
        agent_info['name'] = name
        if farm:
            latest_run = AgentRunModel.get_latest_by_agent(farm['id'], name)
            agent_info['last_run'] = latest_run
        else:
            agent_info['last_run'] = None
        agents_data.append(agent_info)

    return render_template('agents.html', user=user, farm=farm, agents=agents_data)


@agent_bp.route('/agents/<slug>')
@login_required
def agent_detail(slug):
    user = g.user
    farm = FarmModel.get_by_user_id(user['id'])
    agent_name = _slug_to_name(slug)

    if not agent_name:
        flash('Agent not found.', 'error')
        return redirect(url_for('agents.agents_list'))

    meta = AGENT_META[agent_name]
    latest_run = None
    runs_history = []

    if farm:
        latest_run = AgentRunModel.get_latest_by_agent(farm['id'], agent_name)
        all_runs = AgentRunModel.get_all(farm['id'], limit=30)
        runs_history = [r for r in all_runs if r.get('agent_name') == agent_name]

    # Parse output JSON for display
    parsed_output = None
    if latest_run and latest_run.get('output_json'):
        try:
            parsed_output = json.loads(latest_run['output_json'])
        except Exception:
            parsed_output = None

    return render_template('agent_detail.html',
        user=user,
        farm=farm,
        agent_name=agent_name,
        meta=meta,
        latest_run=latest_run,
        parsed_output=parsed_output,
        runs_history=runs_history
    )


@agent_bp.route('/agents/<slug>/run', methods=['POST'])
@login_required
def run_agent(slug):
    """
    Supports both:
      - HTML form POST  → redirect with flash
      - JSON/fetch POST → return JSON response
    """
    user = g.user
    farm = FarmModel.get_by_user_id(user['id'])
    wants_json = (
        request.accept_mimetypes.accept_json
        and not request.accept_mimetypes.accept_html
    ) or request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def _error(msg, status=400):
        if wants_json:
            return jsonify({"error": msg}), status
        flash(msg, 'error')
        return redirect(url_for('farm.farm'))

    if not farm:
        return _error('Please set up your farm profile first.')

    crop = CropModel.get_by_farm_id(farm['id'])
    observation = ObservationModel.get_latest(farm['id'])

    # Agents use sensible defaults if crop/observation not yet recorded
    if not crop:
        crop = {}
    if not observation:
        observation = {}

    agent_name = _slug_to_name(slug)
    if not agent_name:
        return _error('Agent not found.', 404)

    try:
        result = AgentOrchestrator.run_single(farm, crop, observation, agent_name)
    except Exception as e:
        return _error(f'Error running {agent_name}: {str(e)}', 500)

    if wants_json:
        return jsonify({
            "success": True,
            "agent": agent_name,
            "result": result
        })

    flash(f'{agent_name} analysis completed successfully!', 'success')
    return redirect(url_for('agents.agent_detail', slug=slug))


@agent_bp.route('/agents/run-all', methods=['POST'])
@login_required
def run_all_agents():
    user = g.user
    farm = FarmModel.get_by_user_id(user['id'])

    if not farm:
        flash('Please set up your farm profile first.', 'error')
        return redirect(url_for('farm.farm'))

    crop = CropModel.get_by_farm_id(farm['id'])
    observation = ObservationModel.get_latest(farm['id'])

    if not crop:
        crop = {}
    if not observation:
        observation = {}

    try:
        AgentOrchestrator.run_all(farm, crop, observation)
        flash('All AI agents analysis completed successfully!', 'success')
    except Exception as e:
        flash(f'Error during orchestration: {str(e)}', 'error')

    return redirect(url_for('dashboard.overview'))


# ── Per-Agent Q&A ─────────────────────────────────────────────────────────────

# Agent-specific personas, topics, and scope descriptions
AGENT_QA_PERSONAS = {
    'Weather Agent': {
        'persona': (
            "You are the KisanMitra Weather Agent — an expert agricultural meteorologist and climate advisor. "
            "You help farmers understand weather conditions, forecasts, climate impact on crops, irrigation timing based on rain, "
            "frost risk, heat stress, and how to plan farm activities around weather. "
            "Answer only weather, climate, and weather-related farming questions."
        ),
        'scope': "weather, rainfall, temperature, humidity, wind, UV, frost, drought, flood risk, irrigation timing based on rain, seasonal climate",
        'out_of_scope': "If the question is not related to weather or climate, politely say: 'I am the Weather Agent. I can only help with weather and climate-related farming questions. Please ask the Soil Agent, Fertilizer Agent, Market Agent, or another agent for that topic.'"
    },
    'Soil Agent': {
        'persona': (
            "You are the KisanMitra Soil Agent — an expert agronomist and soil scientist. "
            "You help farmers understand soil health, pH, moisture, N-P-K nutrients, organic matter, soil type suitability, "
            "crop suitability for soil conditions, intercropping, soil improvement techniques, and soil-weather interactions. "
            "Answer only soil-related questions."
        ),
        'scope': "soil health, soil pH, soil moisture, nitrogen, phosphorus, potassium, organic matter, soil type, crop suitability for soil, intercropping, soil amendment",
        'out_of_scope': "If the question is not related to soil, nutrients, or land health, politely say: 'I am the Soil Agent. I can only help with soil health and nutrient-related questions. Please ask the relevant agent for that topic.'"
    },
    'Fertilizer Agent': {
        'persona': (
            "You are the KisanMitra Fertilizer Agent — an expert crop nutrition and fertilizer advisor. "
            "You help farmers identify fertilizer needs, nutrient deficiencies, fertilizer types (Urea, DAP, MOP/Potash, SSP, NPK 10:26:26, NPK 19:19:19, Ammonium Sulphate), "
            "application timing, dosage, weather windows for application, and symptoms of nutrient problems. "
            "You also accept questions about yellowing leaves, stunted growth, and other symptoms that may relate to nutrition. "
            "Answer only fertilizer and crop nutrition questions."
        ),
        'scope': "fertilizer, nutrients, N-P-K, urea, DAP, MOP, potash, SSP, NPK, ammonium sulphate, deficiency, toxicity, application timing, dose, yellowing, leaf symptoms",
        'out_of_scope': "If the question is completely unrelated to fertilizer or crop nutrition (e.g. general knowledge, geography, politics), politely say: 'I am the Fertilizer Agent. I can only help with fertilizer and crop nutrition questions. Please ask the relevant agent for other topics.'"
    },
    'Crop Disease Agent': {
        'persona': (
            "You are the KisanMitra Crop Disease Agent — an expert plant pathologist and pest management advisor. "
            "You help farmers identify crop diseases, pest infestations, fungal infections, bacterial infections, viral diseases, "
            "insect damage, weed problems, and recommend treatments and prevention. "
            "Answer only crop health, disease, and pest questions."
        ),
        'scope': "crop disease, leaf spot, blight, rust, mildew, fungal infection, bacterial infection, pest, insect, weed, treatment, fungicide, pesticide, plant health",
        'out_of_scope': "If the question is not about crop disease, pests, or plant health, politely say: 'I am the Crop Disease Agent. I can only help with crop disease and pest-related questions. Please ask the relevant agent for other topics.'"
    },
    'Irrigation Agent': {
        'persona': (
            "You are the KisanMitra Irrigation Agent — an expert in water management and irrigation systems. "
            "You help farmers optimize irrigation schedules, understand water requirements, troubleshoot drip/sprinkler/flood systems, "
            "reduce water waste, and adjust irrigation based on weather and crop stage. "
            "Answer only irrigation and water management questions."
        ),
        'scope': "irrigation, water, drip irrigation, sprinkler, flood irrigation, watering schedule, water stress, drainage, soil moisture, crop water requirement",
        'out_of_scope': "If the question is not related to irrigation or water management, politely say: 'I am the Irrigation Agent. I can only help with irrigation and water management questions. Please ask the relevant agent for other topics.'"
    },
    'Market Agent': {
        'persona': (
            "You are the KisanMitra Market Agent — an expert agricultural market intelligence advisor. "
            "You help farmers understand market prices for vegetables, fruits, flowers, grains, pulses, and other produce. "
            "You analyze price trends, demand-supply dynamics, selling strategies, price increase/decrease implications, "
            "best time to sell, storage vs. sell decisions, and market risk. "
            "Never fabricate current live prices — always label any price as an estimate or historical reference. "
            "Answer only agricultural market, trade, and selling questions."
        ),
        'scope': "market price, mandi, selling, vegetables, fruits, grains, pulses, flowers, demand, supply, price trend, storage, harvest timing, revenue",
        'out_of_scope': "If the question is not about agricultural markets, selling, or produce pricing, politely say: 'I am the Market Agent. I can only help with agricultural market and selling questions. Please ask the relevant agent for other topics.'"
    },
    'Farm Planning Agent': {
        'persona': (
            "You are the KisanMitra Farm Planning Agent — an expert agricultural strategist who synthesizes all farm data into a unified plan. "
            "You help farmers with seasonal planning, crop rotation, resource allocation, risk management, and farm-wide decisions. "
            "You coordinate information from soil, weather, crop, fertilizer, market, and irrigation data. "
            "Answer farm planning, strategy, and overall management questions."
        ),
        'scope': "farm planning, crop rotation, seasonal plan, resource management, risk assessment, overall farm strategy, crop calendar, land use",
        'out_of_scope': "If the question is completely off-topic (e.g. general knowledge unrelated to farming), politely redirect."
    }
}


@agent_bp.route('/agents/<slug>/ask', methods=['POST'])
@login_required
def ask_agent(slug):
    """Let the farmer ask a direct question to a specific agent."""
    user  = g.user
    farm  = FarmModel.get_by_user_id(user['id'])
    wants_json = True  # This endpoint always returns JSON

    agent_name = _slug_to_name(slug)
    if not agent_name:
        return jsonify({"error": "Agent not found."}), 404

    data     = request.get_json(silent=True) or {}
    question = str(data.get('question', '')).strip()
    language = str(data.get('language', user.get('language', 'en') or 'en')).strip()

    if not question:
        return jsonify({"error": "Question is required."}), 400
    if len(question) > 1000:
        return jsonify({"error": "Question is too long (max 1000 characters)."}), 400

    # Build farm context for the answer
    crop        = CropModel.get_by_farm_id(farm['id']) if farm else {}
    observation = ObservationModel.get_latest(farm['id']) if farm else {}
    crop        = crop or {}
    observation = observation or {}

    farm_ctx = ""
    if farm:
        farm_ctx += f"Farm: {farm.get('name','')}, Location: {farm.get('location','')}, Soil: {farm.get('soil_type','')}, Area: {farm.get('area',0)} acres\n"
    if crop:
        farm_ctx += f"Crop: {crop.get('name','')}, Stage: {crop.get('stage','')}, Variety: {crop.get('variety','')}\n"
    if observation:
        farm_ctx += (
            f"Soil Moisture: {observation.get('soil_moisture','')}%, pH: {observation.get('soil_ph','')}\n"
            f"N: {observation.get('nitrogen','')} P: {observation.get('phosphorus','')} K: {observation.get('potassium','')} kg/ha\n"
            f"Temp: {observation.get('temperature','')}°C, Humidity: {observation.get('humidity','')}%, Rainfall: {observation.get('rainfall','')}mm\n"
            f"Crop Health: {observation.get('crop_health','')}%, Notes: {observation.get('disease_notes','')}\n"
            f"Market Price: ₹{observation.get('market_price','')} /q\n"
        )

    # Get latest run from this specific agent for extra context
    latest_run_ctx = ""
    if farm:
        try:
            run = AgentRunModel.get_latest_by_agent(farm['id'], agent_name)
            if run and run.get('output_json'):
                import json as _json
                run_data = _json.loads(run['output_json'])
                summary = run_data.get('summary') or run_data.get('recommendation') or ''
                if summary:
                    latest_run_ctx = f"\nLatest {agent_name} analysis summary: {summary}\n"
        except Exception:
            pass

    # Language directive
    lang_name = LanguageService.get_language_name(language)

    qa = AGENT_QA_PERSONAS.get(agent_name, {})
    system_instruction = (
        (qa.get('persona') or f"You are the {agent_name}, an expert AI advisor for farmers.") +
        f"\n\nIMPORTANT SCOPE RULE: {qa.get('out_of_scope', '')}"
        f"\n\nAlways respond in {lang_name}. Be practical, clear, and farmer-friendly."
    )

    prompt = (
        f"=== FARMER'S FARM CONTEXT ===\n{farm_ctx}"
        f"{latest_run_ctx}\n"
        f"=== FARMER'S QUESTION TO {agent_name.upper()} ===\n{question}\n\n"
        f"Answer as the {agent_name} specialist. If the question is within your scope ({qa.get('scope','')}), "
        f"provide a helpful, practical answer. If it is outside your scope, politely redirect the farmer."
    )

    from services.gemini_service import GeminiService
    try:
        answer = GeminiService.generate_response(prompt=prompt, system_instruction=system_instruction, lang_code=language)
        if not answer or "temporarily unavailable" in answer.lower():
            answer = "I'm unable to respond right now. Please try again in a moment."
    except Exception as e:
        answer = "I'm unable to respond right now. Please try again."

    return jsonify({"success": True, "answer": answer, "agent": agent_name})
