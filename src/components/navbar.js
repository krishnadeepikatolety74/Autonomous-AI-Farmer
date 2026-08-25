/* ===========================================
   NAVBAR Component
   =========================================== */

import { getCurrentRoute } from '../router.js';

export function renderNavbar() {
  const route = getCurrentRoute();

  return `
    <nav class="navbar" id="main-navbar">
      <a href="#/" class="nav-logo">
        <span class="logo-icon">🌿</span>
        <span>AI Farmer</span>
      </a>

      <div class="nav-links">
        <a href="#hero" class="nav-scroll-link">Home</a>
        <a href="#about" class="nav-scroll-link">Overview</a>
        <a href="#agents-section" class="nav-scroll-link">AI Agents</a>
        <a href="#how-it-works" class="nav-scroll-link">How It Works</a>
        <a href="#about" class="nav-scroll-link">About</a>
      </div>

      <div class="nav-right">
        <div class="weather-badge">
          <span class="weather-icon">☀️</span>
          <div>
            <div class="weather-temp">24°C</div>
            <div class="weather-desc">Partly Cloudy</div>
          </div>
        </div>
        <a href="#/signin" class="btn btn-sm btn-outline">Sign In</a>
        <a href="#/signup" class="btn btn-sm btn-primary">Get Started</a>
        <button class="mobile-menu-btn" id="mobile-menu-btn" aria-label="Menu">☰</button>
      </div>
    </nav>
  `;
}

export function initNavbar() {
  // Scroll effect
  const handleScroll = () => {
    const navbar = document.getElementById('main-navbar');
    if (navbar) {
      navbar.classList.toggle('scrolled', window.scrollY > 20);
    }
  };

  window.addEventListener('scroll', handleScroll);
  return () => window.removeEventListener('scroll', handleScroll);
}
