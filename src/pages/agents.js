/* ===========================================
   AI AGENTS PAGE
   =========================================== */

import { renderSidebar, initSidebar } from '../components/sidebar.js';

const agents = [
  {
    id: 'weather',
    name: 'Weather Agent',
    desc: 'Monitoring weather conditions and forecasting impact on crops.',
    image: '/images/agent-weather.png',
    lastRun: 'Last run: 10:15 AM',
    status: 'Low Risk',
    statusType: 'green',
  },
  {
    id: 'soil',
    name: 'Soil Agent',
    desc: 'Analyzing soil health and nutrient levels across all zones.',
    image: '/images/agent-soil.png',
    lastRun: 'Last run: 10:18 AM',
    status: 'Optimal',
    statusType: 'green',
  },
  {
    id: 'crop-disease',
    name: 'Crop Disease Agent',
    desc: 'Checking crop health and identifying potential disease outbreaks.',
    image: '/images/agent-crop-disease.png',
    lastRun: 'Last run: 10:15 AM',
    status: 'Medium Risk',
    statusType: 'yellow',
  },
  {
    id: 'irrigation',
    name: 'Irrigation Agent',
    desc: 'Scheduling intelligent irrigation schedules and water management.',
    image: '/images/agent-irrigation.png',
    lastRun: 'Last run: 10:22 AM',
    status: 'Active',
    statusType: 'green',
  },
  {
    id: 'fertilizer',
    name: 'Fertilizer Agent',
    desc: 'Recommending fertilizer types, quantities and application schedules.',
    image: '/images/agent-fertilizer.png',
    lastRun: 'Last run: 10:30 AM',
    status: 'Scheduled',
    statusType: 'blue',
  },
  {
    id: 'market',
    name: 'Market Agent',
    desc: 'Analyzing market trends and prices for optimal selling decisions.',
    image: '/images/agent-market.png',
    lastRun: 'Last run: 10:17 AM',
    status: 'Rising',
    statusType: 'green',
  },
];

export function renderAgents() {
  const agentCards = agents.map(agent => `
    <div class="agent-card animate-in">
      <div class="agent-icon">
        <img src="${agent.image}" alt="${agent.name}" />
      </div>
      <div>
        <div class="agent-name">${agent.name}</div>
        <div class="agent-desc">${agent.desc}</div>
      </div>
      <div class="agent-meta">
        <span>${agent.lastRun}</span>
        <span class="badge badge-${agent.statusType}" style="align-self: flex-start; margin-top: 4px;">${agent.status}</span>
      </div>
      <a href="#/agent/${agent.id}" class="btn btn-sm btn-secondary" style="align-self: flex-start;">View Analysis</a>
    </div>
  `).join('');

  const html = `
    <div class="dashboard-layout page-transition">
      ${renderSidebar()}

      <main class="dashboard-content">
        <!-- Header -->
        <div class="dashboard-header">
          <div class="header-left">
            <h2>AI Agents</h2>
            <p style="font-size: 13px; margin-top: 4px;">Intelligent agents working together for your farm</p>
          </div>
          <div class="header-right">
            <div class="header-icons">
              <button class="icon-btn" aria-label="Notifications">🔔</button>
              <button class="icon-btn" aria-label="Settings">⚙️</button>
            </div>
          </div>
        </div>

        <!-- Agents Grid -->
        <div class="section">
          <div class="agents-grid">
            ${agentCards}
          </div>
        </div>

        <!-- Farm Planning Agent (Coordinator) -->
        <div class="section">
          <div class="card" style="display: flex; align-items: center; gap: 24px;">
            <div style="width: 100px; height: 100px; border-radius: 18px; overflow: hidden; background: var(--pale-green); flex-shrink: 0;">
              <img src="/images/agent-farm-planning.png" alt="Farm Planning Agent" style="width: 100%; height: 100%; object-fit: cover;" />
            </div>
            <div style="flex: 1;">
              <h4 style="font-size: 16px; margin-bottom: 4px;">Farm Planning Agent (Coordinator)</h4>
              <p style="font-size: 13px;">Combining all insights to create the best plan for your farm.</p>
              <span style="font-size: 11px; color: var(--text-secondary); display: block; margin-top: 4px;">Last run: 10:35 AM</span>
            </div>
            <a href="#/agent/farm-planning" class="btn btn-primary btn-sm">View Final Plan</a>
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
