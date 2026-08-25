/* ===========================================
   HOME PAGE (Public Landing Page)
   =========================================== */

import { renderNavbar, initNavbar } from '../components/navbar.js';
import { createWeatherEnvironment, startWeatherAnimations, stopWeatherAnimations } from '../components/weather-animation.js';

export function renderHome() {
  const html = `
    ${createWeatherEnvironment()}
    ${renderNavbar()}

    <!-- SECTION 2: HERO -->
    <section class="hero page-transition" id="hero">
      <div class="hero-bg">
        <img src="/images/hero-farm.png" alt="Smart Farm Landscape" />
      </div>

      <div class="hero-content">
        <h1>Autonomous<br>AI Farmer</h1>
        <p class="hero-subtitle">Your Intelligent Digital Farm Manager</p>
        <p class="hero-desc">
          Leveraging multi-agent AI technology to monitor, analyze,
          and optimize your farm for higher productivity
          and sustainable farming.
        </p>
        <div class="hero-actions">
          <a href="#/signin" class="btn btn-primary btn-lg">
            🌱 Enter Farm Dashboard
          </a>
          <a href="#agents-section" class="btn btn-secondary btn-lg nav-scroll-link">
            → Explore AI Agents
          </a>
        </div>
      </div>
    </section>

    <!-- SECTION 3: ABOUT -->
    <section class="landing-section" id="about">
      <div class="landing-section-header">
        <h2>Meet Your AI-Powered Farm Manager</h2>
        <p>AI Farmer brings multiple intelligent AI agents together to continuously understand your farm, monitor conditions, identify risks and provide actionable recommendations.</p>
      </div>

      <!-- Flow Chart Visualisation -->
      <div class="card-no-hover" style="background: var(--pale-green); border: 1.5px solid rgba(111,175,123,0.15); margin-bottom: 40px; padding: var(--space-xl); text-align: center;">
        <h4 style="margin-bottom: var(--space-lg); font-size: 18px; color: var(--deep-forest);">Intelligent Decision Flow</h4>
        <div style="display: flex; justify-content: center; align-items: center; gap: 20px; flex-wrap: wrap; font-weight: 600;">
          <div class="badge badge-green" style="padding: 10px 20px; font-size: 14px; box-shadow: var(--shadow-sm);">👨‍🌾 Farmer</div>
          <span style="color: var(--primary); font-size: 20px;">➔</span>
          <div class="badge badge-blue" style="padding: 10px 20px; font-size: 14px; box-shadow: var(--shadow-sm);">🤖 AI Farmer Hub</div>
          <span style="color: var(--primary); font-size: 20px;">➔</span>
          <div class="badge badge-green" style="padding: 10px 20px; font-size: 14px; box-shadow: var(--shadow-sm);">🧠 Multiple AI Agents</div>
          <span style="color: var(--primary); font-size: 20px;">➔</span>
          <div class="badge badge-yellow" style="padding: 10px 20px; font-size: 14px; box-shadow: var(--shadow-sm);">💡 Smart Decisions</div>
        </div>
      </div>

      <div class="benefit-cards-grid">
        <div class="card hover-lift">
          <div style="font-size: 40px; margin-bottom: var(--space-md);">📡</div>
          <h4>Monitor</h4>
          <p style="font-size: 13px; margin-top: var(--space-xs);">Continuously monitor weather, soil, crops and farm conditions in real-time with IoT telemetry.</p>
        </div>
        <div class="card hover-lift">
          <div style="font-size: 40px; margin-bottom: var(--space-md);">🔍</div>
          <h4>Analyze</h4>
          <p style="font-size: 13px; margin-top: var(--space-xs);">AI agents analyze historical and real-time farm data to identify potential risks and yield opportunities.</p>
        </div>
        <div class="card hover-lift">
          <div style="font-size: 40px; margin-bottom: var(--space-md);">📈</div>
          <h4>Optimize</h4>
          <p style="font-size: 13px; margin-top: var(--space-xs);">Get intelligent, automated recommendations for irrigation scheduling, fertilizers, crop health, and market sales.</p>
        </div>
      </div>
    </section>

    <!-- SECTION 4: HOW IT WORKS -->
    <section class="landing-section" id="how-it-works">
      <div class="landing-section-header">
        <h2>How AI Farmer Works</h2>
        <p>Our smart system translates field variables into actionable, high-yielding field operations seamlessly.</p>
      </div>

      <div class="workflow-container">
        <div class="workflow-step">
          <span class="step-icon">📡</span>
          <h5>Farm Data</h5>
          <p style="font-size: 12px; margin-top: 6px; color: var(--text-secondary);">Sensors, weather feeds, satellite data.</p>
          <span class="step-arrow">➔</span>
        </div>
        <div class="workflow-step">
          <span class="step-icon">👁️</span>
          <h5>AI Monitoring</h5>
          <p style="font-size: 12px; margin-top: 6px; color: var(--text-secondary);">24/7 scanning of crop health status.</p>
          <span class="step-arrow">➔</span>
        </div>
        <div class="workflow-step">
          <span class="step-icon">🤖</span>
          <h5>Specialized AI Agents</h5>
          <p style="font-size: 12px; margin-top: 6px; color: var(--text-secondary);">Agents dedicated to soil, water, disease.</p>
          <span class="step-arrow">➔</span>
        </div>
        <div class="workflow-step">
          <span class="step-icon">📊</span>
          <h5>Data Analysis</h5>
          <p style="font-size: 12px; margin-top: 6px; color: var(--text-secondary);">Correlating market and agronomic data.</p>
          <span class="step-arrow">➔</span>
        </div>
        <div class="workflow-step">
          <span class="step-icon">💡</span>
          <h5>AI Recommendations</h5>
          <p style="font-size: 12px; margin-top: 6px; color: var(--text-secondary);">Precise dosages, timings, forecasts.</p>
          <span class="step-arrow">➔</span>
        </div>
        <div class="workflow-step">
          <span class="step-icon">🚜</span>
          <h5>Farmer Decisions</h5>
          <p style="font-size: 12px; margin-top: 6px; color: var(--text-secondary);">Executing smart operations on the field.</p>
        </div>
      </div>
    </section>

    <!-- SECTION 5: AI AGENTS -->
    <section class="landing-section" id="agents-section">
      <div class="landing-section-header">
        <h2>Meet Your AI Farm Team</h2>
        <p>Specialized AI agents working together to make your farm smarter.</p>
      </div>

      <div class="agents-grid" style="margin-bottom: var(--space-xl);">
        <!-- Weather Agent -->
        <div class="agent-card">
          <div class="agent-icon"><img src="/images/agent-weather.png" alt="Weather Agent" /></div>
          <div>
            <div class="agent-name">🌦️ Weather Agent</div>
            <div class="agent-desc">Monitors local weather and climate conditions.</div>
          </div>
        </div>
        <!-- Soil Agent -->
        <div class="agent-card">
          <div class="agent-icon"><img src="/images/agent-soil.png" alt="Soil Agent" /></div>
          <div>
            <div class="agent-name">🌱 Soil Agent</div>
            <div class="agent-desc">Analyzes soil health, telemetry and nutrient levels.</div>
          </div>
        </div>
        <!-- Crop Disease Agent -->
        <div class="agent-card">
          <div class="agent-icon"><img src="/images/agent-crop-disease.png" alt="Crop Disease Agent" /></div>
          <div>
            <div class="agent-name">🌾 Crop Disease Agent</div>
            <div class="agent-desc">Monitors crop health and detects diseases early.</div>
          </div>
        </div>
        <!-- Irrigation Agent -->
        <div class="agent-card">
          <div class="agent-icon"><img src="/images/agent-irrigation.png" alt="Irrigation Agent" /></div>
          <div>
            <div class="agent-name">💧 Irrigation Agent</div>
            <div class="agent-desc">Optimizes water distribution and valve schedules.</div>
          </div>
        </div>
        <!-- Fertilizer Agent -->
        <div class="agent-card">
          <div class="agent-icon"><img src="/images/agent-fertilizer.png" alt="Fertilizer Agent" /></div>
          <div>
            <div class="agent-name">🧪 Fertilizer Agent</div>
            <div class="agent-desc">Generates crop-specific nutrient application plans.</div>
          </div>
        </div>
        <!-- Market Agent -->
        <div class="agent-card">
          <div class="agent-icon"><img src="/images/agent-market.png" alt="Market Agent" /></div>
          <div>
            <div class="agent-name">📈 Market Agent</div>
            <div class="agent-desc">Tracks commodity prices and optimal selling windows.</div>
          </div>
        </div>
      </div>

      <!-- Farm Planning Agent -->
      <div class="card" style="display: flex; align-items: center; gap: 24px;">
        <div style="width: 100px; height: 100px; border-radius: 18px; overflow: hidden; background: var(--pale-green); flex-shrink: 0;">
          <img src="/images/agent-farm-planning.png" alt="Farm Planning Agent" style="width: 100%; height: 100%; object-fit: cover;" />
        </div>
        <div style="flex: 1;">
          <h4 style="font-size: 16px; margin-bottom: 4px;">🧠 Farm Planning Agent (Coordinator)</h4>
          <p style="font-size: 13px;">Coordinates data and conflicts between all agents to synthesize one unified, comprehensive operational strategy.</p>
        </div>
      </div>
    </section>

    <!-- SECTION 7: KEY FEATURES -->
    <section class="landing-section" id="features">
      <div class="landing-section-header">
        <h2>Everything Your Farm Needs</h2>
        <p>A comprehensive ecosystem loaded with premium functionalities built for modern smart farming.</p>
      </div>

      <div class="feature-grid-8">
        <div class="card hover-lift">
          <h5 style="margin-bottom:6px;">🌦️ Smart Weather</h5>
          <p style="font-size:12px; color:var(--text-secondary);">Predictive climate telemetry maps localized alerts to optimize seed scheduling.</p>
        </div>
        <div class="card hover-lift">
          <h5 style="margin-bottom:6px;">🌾 Disease Diagnostics</h5>
          <p style="font-size:12px; color:var(--text-secondary);">Early plant disease detection scanning blocks spread before visual outbreak signs emerge.</p>
        </div>
        <div class="card hover-lift">
          <h5 style="margin-bottom:6px;">💧 Smart Irrigation</h5>
          <p style="font-size:12px; color:var(--text-secondary);">Real-time monitoring triggers water pumps only when soil humidity indices require it.</p>
        </div>
        <div class="card hover-lift">
          <h5 style="margin-bottom:6px;">🧪 Fertilizer Planner</h5>
          <p style="font-size:12px; color:var(--text-secondary);">Custom composition maps calculated directly from target soil mineral analytics.</p>
        </div>
        <div class="card hover-lift">
          <h5 style="margin-bottom:6px;">📊 Farm Analytics</h5>
          <p style="font-size:12px; color:var(--text-secondary);">Visual yield tracking indices, forecast charts, and historical metric memory nodes.</p>
        </div>
        <div class="card hover-lift">
          <h5 style="margin-bottom:6px;">🚨 Risk Alerts</h5>
          <p style="font-size:12px; color:var(--text-secondary);">Receive instant warnings regarding frost, mildew spread, and local mandi price anomalies.</p>
        </div>
        <div class="card hover-lift">
          <h5 style="margin-bottom:6px;">📈 Market Intelligence</h5>
          <p style="font-size:12px; color:var(--text-secondary);">Lock maximum profit windows mapped against live grain demand curves.</p>
        </div>
        <div class="card hover-lift">
          <h5 style="margin-bottom:6px;">🤖 Multi-Agent AI</h5>
          <p style="font-size:12px; color:var(--text-secondary);">Collaborative intelligence loops resolving water budgets and fertilizer costs simultaneously.</p>
        </div>
      </div>
    </section>

    <!-- SECTION 9: WHY CHOOSE -->
    <section class="landing-section" id="why-choose">
      <div class="landing-section-header">
        <h2>Why Choose AI Farmer?</h2>
        <p>A leap forward in agricultural economics, engineered with advanced AI capabilities.</p>
      </div>

      <div class="why-grid">
        <div class="card hover-lift">
          <h5>💡 Smarter Decisions</h5>
          <p style="font-size:13px; color:var(--text-secondary); margin-top:4px;">No more guesswork. Make data-driven decisions backed by live field sensors and historical weather telemetry.</p>
        </div>
        <div class="card hover-lift">
          <h5>👁️ Less Manual Monitoring</h5>
          <p style="font-size:13px; color:var(--text-secondary); margin-top:4px;">Let AI agents handle 24/7 field status checks. Spend less time tracking data and more time farming.</p>
        </div>
        <div class="card hover-lift">
          <h5>🌾 Better Productivity</h5>
          <p style="font-size:13px; color:var(--text-secondary); margin-top:4px;">Optimize fertilizer application windows and watering cycles to maximize seed yields per acre.</p>
        </div>
        <div class="card hover-lift">
          <h5>💧 Sustainable Farming</h5>
          <p style="font-size:13px; color:var(--text-secondary); margin-top:4px;">Reduce chemical runoff, conserve reservoir capacity, and lower operational carbon footprints.</p>
        </div>
      </div>
    </section>

    <!-- SECTION 10: SIMPLE EXPERIENCE -->
    <section class="landing-section" id="experience">
      <div class="landing-section-header">
        <h2>From Data to Decision in Seconds</h2>
        <p>Get started with smart farming in three simple steps.</p>
      </div>

      <div class="experience-steps">
        <div class="experience-step-card">
          <div class="step-num">01</div>
          <h5>Connect Your Farm</h5>
          <p style="font-size:13px; color:var(--text-secondary); margin-top:6px;">Register your fields, select your seed types, and connect any existing IoT telemetry feeds.</p>
        </div>
        <div class="experience-step-card">
          <div class="step-num">02</div>
          <h5>Let AI Analyze</h5>
          <p style="font-size:13px; color:var(--text-secondary); margin-top:6px;">Your autonomous agent loops continuously scan local climate data and soil moisture states.</p>
        </div>
        <div class="experience-step-card">
          <div class="step-num">03</div>
          <h5>Take Action</h5>
          <p style="font-size:13px; color:var(--text-secondary); margin-top:6px;">Receive optimized, yield-mapped task lists and alerts straight to your digital dashboard.</p>
        </div>
      </div>
    </section>

    <!-- SECTION 11: FINAL CALL TO ACTION -->
    <section class="landing-section">
      <div class="cta-banner">
        <h2 style="font-size:32px; color:var(--deep-forest); margin-bottom:12px;">Ready to Make Your Farm Smarter?</h2>
        <p style="color:var(--text-secondary); max-width:500px; margin: 0 auto 24px; font-size:16px;">
          Join thousands of agricultural managers using AI Farmer to maximize productivity.
        </p>
        <div style="display:flex; justify-content:center; gap:var(--space-md); flex-wrap:wrap;">
          <a href="#/signup" class="btn btn-primary btn-lg">Create Your AI Farmer Account</a>
          <a href="#/signin" class="btn btn-secondary btn-lg">Already Have an Account? Sign In</a>
        </div>
      </div>
    </section>

    <!-- SECTION 12: FOOTER -->
    <footer class="footer">
      <div class="footer-grid">
        <div class="footer-col">
          <h4 style="font-size:18px; color:var(--deep-forest); margin-bottom: 10px;">🌿 AI Farmer</h4>
          <p style="font-size:13px; color:var(--text-secondary); line-height:1.6;">
            Autonomous AI systems engineered for smarter, high-yield sustainable agricultural operations.
          </p>
        </div>
        <div class="footer-col">
          <h4>Product</h4>
          <ul>
            <li><a href="#about" class="nav-scroll-link">Overview</a></li>
            <li><a href="#agents-section" class="nav-scroll-link">AI Agents</a></li>
            <li><a href="#features" class="nav-scroll-link">Features</a></li>
            <li><a href="#/dashboard">Dashboard</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Company</h4>
          <ul>
            <li><a href="#about" class="nav-scroll-link">About Us</a></li>
            <li><a href="#/signin">Contact</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Account</h4>
          <ul>
            <li><a href="#/signin">Sign In</a></li>
            <li><a href="#/signup">Sign Up</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        © 2026 AI Farmer. All rights reserved. Designed for elite smart farm automation.
      </div>
    </footer>
  `;

  return {
    html,
    init: () => {
      const cleanupNavbar = initNavbar();
      startWeatherAnimations();

      // Smooth scroll triggers
      const setupScroll = () => {
        document.querySelectorAll('.nav-scroll-link').forEach(link => {
          link.addEventListener('click', (e) => {
            const targetId = link.getAttribute('href');
            if (targetId.startsWith('#') && targetId.length > 1) {
              const targetEl = document.querySelector(targetId);
              if (targetEl) {
                e.preventDefault();
                targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
              }
            }
          });
        });
      };
      
      setupScroll();

      return () => {
        cleanupNavbar();
        stopWeatherAnimations();
      };
    }
  };
}
