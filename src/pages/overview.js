/* ===========================================
   OVERVIEW PAGE
   =========================================== */

import { renderNavbar, initNavbar } from '../components/navbar.js';
import { createWeatherEnvironment, startWeatherAnimations, stopWeatherAnimations } from '../components/weather-animation.js';

export function renderOverview() {
  const html = `
    ${createWeatherEnvironment()}
    ${renderNavbar()}

    <main class="page-public page-transition" style="position: relative; z-index: 1;">
      <div style="max-width: var(--max-content); margin: 0 auto; padding: var(--space-xl) var(--space-2xl);">

        <!-- Hero Banner -->
        <div class="overview-hero">
          <img src="/images/hero-farm.png" alt="Green Valley Farm" />
          <div class="overview-hero-overlay">
            <div class="overview-hero-content">
              <h2>Green Valley Farm</h2>
              <p>Your intelligent AI-powered farm management overview. Monitor all aspects of your farm in real-time.</p>
            </div>
          </div>
        </div>

        <!-- Quick Stats -->
        <div class="section">
          <div class="section-header">
            <h3 class="section-title">Farm Health Summary</h3>
            <span class="badge badge-green">All Systems Active</span>
          </div>

          <div class="stats-grid stats-grid-4">
            <div class="stat-card animate-in hover-lift">
              <span class="stat-label">Overall Farm Health</span>
              <span class="stat-value" style="color: var(--primary);">82%</span>
              <div class="progress-bar">
                <div class="progress-fill" style="width: 82%;"></div>
              </div>
              <span class="badge badge-green" style="align-self: flex-start; margin-top: 4px;">Good</span>
            </div>
            <div class="stat-card animate-in hover-lift">
              <span class="stat-label">Soil Quality Index</span>
              <span class="stat-value">63%</span>
              <div class="progress-bar">
                <div class="progress-fill" style="width: 63%;"></div>
              </div>
              <span class="badge badge-green" style="align-self: flex-start; margin-top: 4px;">Optimal</span>
            </div>
            <div class="stat-card animate-in hover-lift">
              <span class="stat-label">Water Efficiency</span>
              <span class="stat-value" style="color: var(--blue-weather);">87%</span>
              <div class="progress-bar">
                <div class="progress-fill" style="width: 87%; background: var(--blue-weather);"></div>
              </div>
              <span class="badge badge-blue" style="align-self: flex-start; margin-top: 4px;">Excellent</span>
            </div>
            <div class="stat-card animate-in hover-lift">
              <span class="stat-label">AI Agent Activity</span>
              <span class="stat-value">7/7</span>
              <div class="progress-bar">
                <div class="progress-fill" style="width: 100%;"></div>
              </div>
              <span class="badge badge-green" style="align-self: flex-start; margin-top: 4px;">All Active</span>
            </div>
          </div>
        </div>

        <!-- Crop Performance -->
        <div class="section">
          <div class="section-header">
            <h3 class="section-title">Crop Performance</h3>
          </div>

          <div class="stats-grid" style="grid-template-columns: repeat(3, 1fr);">
            <div class="card hover-lift animate-in">
              <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
                <div style="width: 48px; height: 48px; border-radius: 14px; background: var(--soft-mint); display: flex; align-items: center; justify-content: center; font-size: 24px;">🌾</div>
                <div>
                  <h4>Wheat</h4>
                  <p style="font-size: 12px;">Zone A • 120 acres</p>
                </div>
              </div>
              <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="font-size: 13px; color: var(--text-secondary);">Growth Stage</span>
                <span class="badge badge-green">Vegetative</span>
              </div>
              <div style="display: flex; justify-content: space-between;">
                <span style="font-size: 13px; color: var(--text-secondary);">Yield Forecast</span>
                <span style="font-size: 14px; font-weight: 600; color: var(--primary);">4.2 t/ha</span>
              </div>
            </div>

            <div class="card hover-lift animate-in">
              <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
                <div style="width: 48px; height: 48px; border-radius: 14px; background: var(--warning-bg); display: flex; align-items: center; justify-content: center; font-size: 24px;">🌽</div>
                <div>
                  <h4>Corn</h4>
                  <p style="font-size: 12px;">Zone B • 80 acres</p>
                </div>
              </div>
              <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="font-size: 13px; color: var(--text-secondary);">Growth Stage</span>
                <span class="badge badge-yellow">Flowering</span>
              </div>
              <div style="display: flex; justify-content: space-between;">
                <span style="font-size: 13px; color: var(--text-secondary);">Yield Forecast</span>
                <span style="font-size: 14px; font-weight: 600; color: var(--primary);">9.1 t/ha</span>
              </div>
            </div>

            <div class="card hover-lift animate-in">
              <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
                <div style="width: 48px; height: 48px; border-radius: 14px; background: var(--pale-green); display: flex; align-items: center; justify-content: center; font-size: 24px;">🫘</div>
                <div>
                  <h4>Soybeans</h4>
                  <p style="font-size: 12px;">Zone C • 60 acres</p>
                </div>
              </div>
              <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="font-size: 13px; color: var(--text-secondary);">Growth Stage</span>
                <span class="badge badge-green">Pod Fill</span>
              </div>
              <div style="display: flex; justify-content: space-between;">
                <span style="font-size: 13px; color: var(--text-secondary);">Yield Forecast</span>
                <span style="font-size: 14px; font-weight: 600; color: var(--primary);">3.5 t/ha</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent AI Recommendations -->
        <div class="section">
          <div class="section-header">
            <h3 class="section-title">Recent AI Recommendations</h3>
            <a href="#/agents" class="btn btn-sm btn-outline">View All Agents →</a>
          </div>

          <div style="display: flex; flex-direction: column; gap: 12px;">
            <div class="card-no-hover" style="display: flex; align-items: center; gap: 16px;">
              <div style="width: 42px; height: 42px; border-radius: 12px; background: var(--blue-weather-bg); display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0;">💧</div>
              <div style="flex: 1;">
                <h4 style="margin-bottom: 2px;">Irrigation Scheduled — Zone A</h4>
                <p style="font-size: 12px;">AI recommends irrigation in 2 days based on soil moisture trends and weather forecast.</p>
              </div>
              <span class="badge badge-blue">Irrigation Agent</span>
              <span style="font-size: 11px; color: var(--text-secondary); white-space: nowrap;">2 hours ago</span>
            </div>

            <div class="card-no-hover" style="display: flex; align-items: center; gap: 16px;">
              <div style="width: 42px; height: 42px; border-radius: 12px; background: var(--warning-bg); display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0;">🧪</div>
              <div style="flex: 1;">
                <h4 style="margin-bottom: 2px;">Fertilizer Application — Zone B</h4>
                <p style="font-size: 12px;">Nitrogen levels are below optimal. Apply 40kg/ha of urea within the next 5 days.</p>
              </div>
              <span class="badge badge-yellow">Fertilizer Agent</span>
              <span style="font-size: 11px; color: var(--text-secondary); white-space: nowrap;">5 hours ago</span>
            </div>

            <div class="card-no-hover" style="display: flex; align-items: center; gap: 16px;">
              <div style="width: 42px; height: 42px; border-radius: 12px; background: var(--soft-mint); display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0;">🛡️</div>
              <div style="flex: 1;">
                <h4 style="margin-bottom: 2px;">Disease Alert — Low Risk Detected</h4>
                <p style="font-size: 12px;">Early signs of powdery mildew detected in Zone C. Preventive treatment recommended.</p>
              </div>
              <span class="badge badge-green">Crop Disease Agent</span>
              <span style="font-size: 11px; color: var(--text-secondary); white-space: nowrap;">1 day ago</span>
            </div>
          </div>
        </div>

        <!-- CTA -->
        <div style="text-align: center; padding: 48px 0;">
          <h3 style="margin-bottom: 12px;">Ready to dive deeper?</h3>
          <p style="margin-bottom: 24px; max-width: 480px; margin-left: auto; margin-right: auto;">
            Access your full dashboard for detailed analytics, AI agent reports, and real-time farm monitoring.
          </p>
          <a href="#/dashboard" class="btn btn-primary btn-lg">Open Dashboard →</a>
        </div>

      </div>
    </main>
  `;

  return {
    html,
    init: () => {
      const cleanupNavbar = initNavbar();
      startWeatherAnimations();
      return () => {
        cleanupNavbar();
        stopWeatherAnimations();
      };
    }
  };
}
