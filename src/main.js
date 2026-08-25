/* ===========================================
   MAIN — Entry Point
   =========================================== */

import { registerRoute, initRouter } from './router.js';
import { renderHome } from './pages/home.js';
import { renderOverview } from './pages/overview.js';
import { renderSignIn } from './pages/signin.js';
import { renderSignUp } from './pages/signup.js';
import { renderDashboard } from './pages/dashboard.js';
import { renderAgents } from './pages/agents.js';
import { renderAgentDetail } from './pages/agent-detail.js';

// Register all routes
registerRoute('/', () => renderHome());
registerRoute('/overview', () => renderOverview());
registerRoute('/signin', () => renderSignIn());
registerRoute('/signup', () => renderSignUp());
registerRoute('/dashboard', () => renderDashboard());
registerRoute('/agents', () => renderAgents());
registerRoute('/agent/:id', (params) => renderAgentDetail(params));

// Initialize router
initRouter();

// Set page title based on route
window.addEventListener('hashchange', () => {
  const titles = {
    '/': 'Autonomous AI Farmer',
    '/overview': 'Farm Overview — AI Farmer',
    '/signin': 'Sign In — AI Farmer',
    '/signup': 'Sign Up — AI Farmer',
    '/dashboard': 'Dashboard — AI Farmer',
    '/agents': 'AI Agents — AI Farmer',
  };

  const hash = window.location.hash.slice(1) || '/';
  const baseRoute = '/' + hash.split('/').filter(Boolean).slice(0, 1).join('/');

  if (hash.startsWith('/agent/')) {
    document.title = 'Agent Detail — AI Farmer';
  } else {
    document.title = titles[hash] || 'Autonomous AI Farmer';
  }
});
