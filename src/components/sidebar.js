/* ===========================================
   SIDEBAR Component
   =========================================== */

import { getCurrentRoute } from '../router.js';

const navItems = [
  { icon: '📊', label: 'Overview', route: '/dashboard', id: 'overview' },
  { icon: '🏠', label: 'Home', route: '/', id: 'home' },
  { icon: '🌾', label: 'My Farm', route: '/overview', id: 'myfarm' },
  { icon: '🤖', label: 'AI Agents', route: '/agents', id: 'agents' },
  { icon: '💡', label: 'Recommendations', route: '/dashboard', id: 'recommendations' },
  { icon: '🧠', label: 'Farm Memory', route: '/dashboard', id: 'memory' },
  { icon: '📈', label: 'Activity', route: '/dashboard', id: 'activity' },
  { icon: '⚙️', label: 'Settings', route: '/dashboard', id: 'settings' },
];

// Map current route to which sidebar item should be active
function getActiveId(route) {
  if (route === '/dashboard') return 'overview';
  if (route === '/') return 'home';
  if (route === '/overview') return 'myfarm';
  if (route === '/agents' || route.startsWith('/agent/')) return 'agents';
  return 'overview';
}

export function renderSidebar() {
  const route = getCurrentRoute();
  const activeId = getActiveId(route);

  const navItemsHtml = navItems.map(item => `
    <a href="#${item.route}" class="nav-item ${item.id === activeId ? 'active' : ''}" data-route="${item.route}">
      <span class="nav-icon">${item.icon}</span>
      <span>${item.label}</span>
    </a>
  `).join('');

  return `
    <aside class="sidebar" id="sidebar">
      <div class="sidebar-logo">
        <span class="logo-icon">🌾</span>
        <span>AI Farmer</span>
      </div>

      <div class="sidebar-user">
        <div class="user-avatar">JF</div>
        <div class="user-info">
          <span class="user-name">John Farmer</span>
          <span class="user-role">Farm Manager</span>
        </div>
        <span style="margin-left: auto; color: var(--text-secondary); font-size: 12px;">›</span>
      </div>

      <nav class="sidebar-nav">
        ${navItemsHtml}
      </nav>

      <div class="sidebar-footer">
        <a href="#/signin" class="nav-item">
          <span class="nav-icon">🚪</span>
          <span>Logout</span>
        </a>
      </div>
    </aside>
    <div class="sidebar-overlay" id="sidebar-overlay"></div>
  `;
}

export function initSidebar() {
  const overlay = document.getElementById('sidebar-overlay');
  const sidebar = document.getElementById('sidebar');

  if (overlay && sidebar) {
    overlay.addEventListener('click', () => {
      sidebar.classList.remove('open');
      overlay.classList.remove('active');
    });
  }
}
