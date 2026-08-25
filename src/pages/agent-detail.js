/* ===========================================
   AGENT DETAIL PAGE
   =========================================== */

import { renderSidebar, initSidebar } from '../components/sidebar.js';

const agentData = {
  'weather': {
    name: 'Weather Agent',
    desc: 'Monitoring weather conditions, forecasting precipitation, temperature trends, and assessing weather-related risks to your crops.',
    image: '/images/agent-weather.png',
    status: 'Active',
    statusType: 'green',
    lastRun: '10:15 AM',
    metrics: [
      { label: 'Temperature', value: '24°C', icon: '🌡️', trend: '+2°C from yesterday' },
      { label: 'Humidity', value: '68%', icon: '💧', trend: 'Normal range' },
      { label: 'Wind Speed', value: '12 km/h', icon: '💨', trend: 'Light breeze' },
      { label: 'Rain Probability', value: '15%', icon: '🌧️', trend: 'Low risk today' },
    ],
    analysis: [
      { title: 'Weather Forecast', desc: 'Clear skies expected for the next 3 days. Temperature will range between 22-28°C. Ideal conditions for crop growth.', type: 'green' },
      { title: 'Frost Warning', desc: 'No frost risk for the next 2 weeks. Minimum temperature expected to stay above 15°C.', type: 'green' },
      { title: 'Storm Alert', desc: 'Potential light rain expected in 5-7 days. Consider completing any outdoor operations before then.', type: 'yellow' },
    ],
    recommendations: [
      'Continue regular irrigation schedule for the next 3 days.',
      'Optimal window for fertilizer application in the next 48 hours.',
      'Plan harvest activities before potential rain in 5-7 days.',
    ]
  },
  'soil': {
    name: 'Soil Agent',
    desc: 'Analyzing soil composition, moisture levels, pH balance, and nutrient content across all farm zones for optimal crop growth.',
    image: '/images/agent-soil.png',
    status: 'Optimal',
    statusType: 'green',
    lastRun: '10:18 AM',
    metrics: [
      { label: 'Soil Moisture', value: '63%', icon: '💧', trend: 'Optimal range' },
      { label: 'pH Level', value: '6.5', icon: '⚗️', trend: 'Slightly acidic' },
      { label: 'Nitrogen', value: '42 ppm', icon: '🧪', trend: 'Needs supplement' },
      { label: 'Organic Matter', value: '3.8%', icon: '🌱', trend: 'Good level' },
    ],
    analysis: [
      { title: 'Zone A — Wheat Field', desc: 'Soil moisture is optimal at 65%. Nitrogen levels are slightly below recommended range. Consider targeted urea application.', type: 'yellow' },
      { title: 'Zone B — Corn Field', desc: 'Excellent soil conditions. pH balanced at 6.4. All nutrient levels within optimal range.', type: 'green' },
      { title: 'Zone C — Soybeans', desc: 'Moisture trending lower than optimal. May need irrigation within 48 hours if no rainfall.', type: 'yellow' },
    ],
    recommendations: [
      'Apply 40 kg/ha nitrogen supplement to Zone A within 5 days.',
      'Monitor Zone C moisture levels — irrigation may be needed.',
      'Soil quality excellent in Zone B — maintain current practices.',
    ]
  },
  'crop-disease': {
    name: 'Crop Disease Agent',
    desc: 'Monitoring crop health, detecting early disease signs, pest identification, and recommending preventive treatments.',
    image: '/images/agent-crop-disease.png',
    status: 'Medium Risk',
    statusType: 'yellow',
    lastRun: '10:15 AM',
    metrics: [
      { label: 'Disease Risk', value: '20%', icon: '🛡️', trend: 'Low-Medium' },
      { label: 'Pest Activity', value: 'Low', icon: '🐛', trend: 'Monitoring' },
      { label: 'Crop Health', value: '82%', icon: '🌿', trend: 'Good overall' },
      { label: 'Treatment Status', value: 'Pending', icon: '💊', trend: 'Preventive' },
    ],
    analysis: [
      { title: 'Powdery Mildew — Zone C', desc: 'Early signs of powdery mildew detected on soybean leaves. Confidence: 73%. Recommend preventive fungicide application within 48 hours.', type: 'yellow' },
      { title: 'Aphid Monitoring — Zone B', desc: 'Low aphid population detected. Currently below economic threshold. Continue monitoring.', type: 'green' },
      { title: 'Wheat Health — Zone A', desc: 'No disease indicators detected. Crop health excellent at 89%.', type: 'green' },
    ],
    recommendations: [
      'Apply preventive fungicide treatment in Zone C within 48 hours.',
      'Continue pest monitoring in Zone B — next check in 3 days.',
      'No action needed for Zone A — crop health is excellent.',
    ]
  },
  'irrigation': {
    name: 'Irrigation Agent',
    desc: 'Managing water resources, scheduling irrigation cycles, monitoring soil moisture, and optimizing water usage efficiency.',
    image: '/images/agent-irrigation.png',
    status: 'Active',
    statusType: 'green',
    lastRun: '10:22 AM',
    metrics: [
      { label: 'Water Usage Today', value: '1,250 L', icon: '💧', trend: '15% below budget' },
      { label: 'Efficiency', value: '87%', icon: '📊', trend: 'Excellent' },
      { label: 'Next Irrigation', value: '2 days', icon: '📅', trend: 'Zone A scheduled' },
      { label: 'Reservoir Level', value: '78%', icon: '🏊', trend: 'Adequate' },
    ],
    analysis: [
      { title: 'Zone A Schedule', desc: 'Irrigation scheduled in 2 days based on current soil moisture trends and weather forecast. Estimated 800L needed.', type: 'blue' },
      { title: 'Zone B Status', desc: 'Adequate moisture levels. No irrigation needed for 4-5 days.', type: 'green' },
      { title: 'Water Conservation', desc: 'Current efficiency at 87%, exceeding target of 80%. Smart scheduling has saved 2,400L this week.', type: 'green' },
    ],
    recommendations: [
      'Schedule Zone A irrigation for day after tomorrow, early morning.',
      'Continue drip irrigation in Zone C at current rate.',
      'Check irrigation system pressure — routine maintenance due.',
    ]
  },
  'fertilizer': {
    name: 'Fertilizer Agent',
    desc: 'Recommending optimal fertilizer compositions, application timing, quantities, and techniques for each crop zone.',
    image: '/images/agent-fertilizer.png',
    status: 'Scheduled',
    statusType: 'blue',
    lastRun: '10:30 AM',
    metrics: [
      { label: 'N Level', value: '42 ppm', icon: '🧪', trend: 'Below optimal' },
      { label: 'P Level', value: '28 ppm', icon: '🧪', trend: 'Normal' },
      { label: 'K Level', value: '35 ppm', icon: '🧪', trend: 'Adequate' },
      { label: 'Application Due', value: '3 days', icon: '📅', trend: 'Zone A priority' },
    ],
    analysis: [
      { title: 'Nitrogen Deficiency — Zone A', desc: 'Nitrogen levels at 42 ppm, below the optimal 55-65 ppm range for wheat at vegetative stage. Application of 40 kg/ha urea recommended.', type: 'yellow' },
      { title: 'Zone B — Balanced', desc: 'All nutrient levels within recommended ranges for corn flowering stage. No additional fertilizer needed.', type: 'green' },
      { title: 'Cost Optimization', desc: 'By timing application with predicted rainfall, absorption can increase by 15% and reduce total fertilizer cost by 8%.', type: 'green' },
    ],
    recommendations: [
      'Apply urea (46-0-0) at 40 kg/ha to Zone A within 5 days.',
      'Time application before forecasted light rain for better absorption.',
      'No fertilizer action needed for Zones B and C at this time.',
    ]
  },
  'market': {
    name: 'Market Agent',
    desc: 'Tracking commodity prices, market trends, demand forecasts, and optimal selling windows for your harvested crops.',
    image: '/images/agent-market.png',
    status: 'Rising',
    statusType: 'green',
    lastRun: '10:17 AM',
    metrics: [
      { label: 'Wheat Price', value: '₹2,450/q', icon: '📈', trend: '+3.2% this week' },
      { label: 'Corn Price', value: '₹1,890/q', icon: '📊', trend: '+1.5% this week' },
      { label: 'Soybean Price', value: '₹4,120/q', icon: '📈', trend: '+4.1% this week' },
      { label: 'Market Sentiment', value: 'Bullish', icon: '🐂', trend: 'Strong demand' },
    ],
    analysis: [
      { title: 'Wheat Market Outlook', desc: 'Wheat prices trending upward due to reduced global supply forecasts. Current price ₹2,450/quintal. Recommend holding for 2-3 weeks for potential 5-8% additional gain.', type: 'green' },
      { title: 'Soybean Opportunity', desc: 'Soybean prices at 6-month high. If harvest is ready, consider selling 60-70% of inventory now to lock in profits.', type: 'green' },
      { title: 'Input Cost Alert', desc: 'Fertilizer prices expected to rise 5% next month. Consider purchasing inputs now.', type: 'yellow' },
    ],
    recommendations: [
      'Hold wheat harvest for 2-3 weeks — prices expected to rise further.',
      'Consider selling 60-70% of soybean inventory at current high prices.',
      'Pre-purchase fertilizer inputs before expected price increase.',
    ]
  },
  'farm-planning': {
    name: 'Farm Planning Agent',
    desc: 'Coordinating all AI agent insights to create a comprehensive, optimized farm management plan with prioritized actions.',
    image: '/images/agent-farm-planning.png',
    status: 'Plan Ready',
    statusType: 'green',
    lastRun: '10:35 AM',
    metrics: [
      { label: 'Actions Pending', value: '5', icon: '📋', trend: 'Priority items' },
      { label: 'Farm Score', value: '82%', icon: '⭐', trend: 'Good condition' },
      { label: 'Risk Level', value: 'Low', icon: '🛡️', trend: 'Manageable' },
      { label: 'Forecast', value: 'Positive', icon: '📈', trend: 'Good outlook' },
    ],
    analysis: [
      { title: 'Priority 1: Zone C Disease Prevention', desc: 'Apply preventive fungicide treatment within 48 hours. Early powdery mildew signs detected. This is the most time-sensitive action.', type: 'yellow' },
      { title: 'Priority 2: Zone A Fertilizer Application', desc: 'Apply nitrogen supplement within 5 days. Time with predicted light rain for optimal absorption.', type: 'yellow' },
      { title: 'Priority 3: Irrigation Schedule', desc: 'Zone A irrigation in 2 days. All other zones have adequate moisture for 4+ days.', type: 'blue' },
      { title: 'Market Strategy', desc: 'Hold wheat, sell soybeans at current highs, pre-purchase fertilizer inputs. Overall positive market outlook.', type: 'green' },
    ],
    recommendations: [
      'Day 1-2: Apply fungicide in Zone C (most urgent).',
      'Day 2-3: Schedule and execute Zone A irrigation.',
      'Day 3-5: Apply nitrogen fertilizer in Zone A.',
      'This week: Sell 60-70% soybean inventory at current market highs.',
      'This week: Pre-purchase fertilizer for next cycle before price rise.',
    ]
  },
};

export function renderAgentDetail(params) {
  const agentId = params.id;
  const agent = agentData[agentId];

  if (!agent) {
    return {
      html: `
        <div class="dashboard-layout page-transition">
          ${renderSidebar()}
          <main class="dashboard-content">
            <a href="#/agents" class="back-link">← Back to AI Agents</a>
            <h2>Agent Not Found</h2>
            <p>The requested agent could not be found.</p>
          </main>
        </div>
      `,
      init: () => { initSidebar(); return () => {}; }
    };
  }

  const metricsHtml = agent.metrics.map(m => `
    <div class="stat-card animate-in hover-lift">
      <div style="display: flex; align-items: center; gap: 8px;">
        <span style="font-size: 20px;">${m.icon}</span>
        <span class="stat-label">${m.label}</span>
      </div>
      <span class="stat-value">${m.value}</span>
      <span style="font-size: 11px; color: var(--text-secondary);">${m.trend}</span>
    </div>
  `).join('');

  const analysisHtml = agent.analysis.map(a => `
    <div class="card-no-hover" style="margin-bottom: 12px;">
      <div style="display: flex; align-items: flex-start; gap: 12px;">
        <span class="badge badge-${a.type}" style="margin-top: 2px; flex-shrink: 0;">
          ${a.type === 'green' ? '✅' : a.type === 'yellow' ? '⚠️' : a.type === 'blue' ? 'ℹ️' : '❌'}
        </span>
        <div>
          <h4 style="margin-bottom: 4px;">${a.title}</h4>
          <p style="font-size: 13px;">${a.desc}</p>
        </div>
      </div>
    </div>
  `).join('');

  const recsHtml = agent.recommendations.map((r, i) => `
    <div style="display: flex; align-items: flex-start; gap: 12px; padding: 12px 0; ${i < agent.recommendations.length - 1 ? 'border-bottom: 1px solid var(--pale-green);' : ''}">
      <span style="width: 24px; height: 24px; border-radius: 50%; background: var(--soft-mint); display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; color: var(--deep-forest); flex-shrink: 0;">${i + 1}</span>
      <p style="font-size: 13px; color: var(--text); line-height: 1.5;">${r}</p>
    </div>
  `).join('');

  const html = `
    <div class="dashboard-layout page-transition">
      ${renderSidebar()}

      <main class="dashboard-content">
        <a href="#/agents" class="back-link">← Back to AI Agents</a>

        <!-- Agent Header -->
        <div class="agent-detail-header">
          <div class="agent-detail-icon">
            <img src="${agent.image}" alt="${agent.name}" />
          </div>
          <div class="agent-detail-info" style="flex: 1;">
            <h2 style="font-size: 28px;">${agent.name}</h2>
            <p>${agent.desc}</p>
            <div style="display: flex; align-items: center; gap: 12px; margin-top: 8px;">
              <span class="badge badge-${agent.statusType}">${agent.status}</span>
              <span style="font-size: 12px; color: var(--text-secondary);">Last run: ${agent.lastRun}</span>
            </div>
          </div>
          <button class="btn btn-primary btn-sm">🔄 Run Analysis</button>
        </div>

        <!-- Metrics -->
        <div class="section">
          <div class="section-header">
            <h3 class="section-title">Key Metrics</h3>
          </div>
          <div class="detail-metric-grid" style="grid-template-columns: repeat(4, 1fr);">
            ${metricsHtml}
          </div>
        </div>

        <!-- Detail Grid: Analysis + Recommendations -->
        <div class="detail-grid">
          <div class="section">
            <div class="section-header">
              <h3 class="section-title">Analysis Results</h3>
            </div>
            ${analysisHtml}
          </div>

          <div class="section">
            <div class="section-header">
              <h3 class="section-title">Recommendations</h3>
            </div>
            <div class="card-no-hover">
              ${recsHtml}
            </div>

            ${agentId === 'fertilizer' ? `
            <!-- Essential Fertilizers Guide -->
            <div class="card-no-hover" style="margin-top: var(--space-xl);">
              <h3 style="color: var(--deep-forest); margin-bottom: var(--space-md); padding-bottom: 8px; border-bottom: 1px solid rgba(0,0,0,0.06); font-size: 16px;">
                🧪 Essential Fertilizers Guide
              </h3>
              <div style="display: flex; flex-direction: column; gap: 8px;">
                <div style="padding: 10px; background: var(--bg); border-radius: 10px; display: flex; justify-content: space-between; align-items: center; font-size: 13px;">
                  <span style="font-weight: 600; color: var(--deep-forest);">1. Urea</span>
                  <span class="badge badge-green" style="font-size: 10px; padding: 2px 8px; background: var(--pale-green); color: var(--primary);">Nitrogen (46%)</span>
                </div>
                <div style="padding: 10px; background: var(--bg); border-radius: 10px; display: flex; justify-content: space-between; align-items: center; font-size: 13px;">
                  <span style="font-weight: 600; color: var(--deep-forest);">2. DAP</span>
                  <span class="badge badge-green" style="font-size: 10px; padding: 2px 8px; background: var(--pale-green); color: var(--primary);">N-P (18-46-0)</span>
                </div>
                <div style="padding: 10px; background: var(--bg); border-radius: 10px; display: flex; justify-content: space-between; align-items: center; font-size: 13px;">
                  <span style="font-weight: 600; color: var(--deep-forest);">3. MOP / Potash</span>
                  <span class="badge badge-green" style="font-size: 10px; padding: 2px 8px; background: var(--pale-green); color: var(--primary);">Potassium (60%)</span>
                </div>
                <div style="padding: 10px; background: var(--bg); border-radius: 10px; display: flex; justify-content: space-between; align-items: center; font-size: 13px;">
                  <span style="font-weight: 600; color: var(--deep-forest);">4. SSP</span>
                  <span class="badge badge-green" style="font-size: 10px; padding: 2px 8px; background: var(--pale-green); color: var(--primary);">P-S-Ca (0-16-0)</span>
                </div>
                <div style="padding: 10px; background: var(--bg); border-radius: 10px; display: flex; justify-content: space-between; align-items: center; font-size: 13px;">
                  <span style="font-weight: 600; color: var(--deep-forest);">5. NPK 10:26:26</span>
                  <span class="badge badge-green" style="font-size: 10px; padding: 2px 8px; background: var(--pale-green); color: var(--primary);">N-P-K Complex</span>
                </div>
                <div style="padding: 10px; background: var(--bg); border-radius: 10px; display: flex; justify-content: space-between; align-items: center; font-size: 13px;">
                  <span style="font-weight: 600; color: var(--deep-forest);">6. NPK 19:19:19</span>
                  <span class="badge badge-green" style="font-size: 10px; padding: 2px 8px; background: var(--pale-green); color: var(--primary);">Balanced N-P-K</span>
                </div>
                <div style="padding: 10px; background: var(--bg); border-radius: 10px; display: flex; justify-content: space-between; align-items: center; font-size: 13px;">
                  <span style="font-weight: 600; color: var(--deep-forest);">7. Ammonium Sulphate</span>
                  <span class="badge badge-green" style="font-size: 10px; padding: 2px 8px; background: var(--pale-green); color: var(--primary);">N-S (21-0-0)</span>
                </div>
              </div>
            </div>
            ` : ''}
          </div>
        </div>
      </main>
    </div>
  `;

  return {
    html,
    init: () => {
      initSidebar();
      return () => {};
    }
  };
}
