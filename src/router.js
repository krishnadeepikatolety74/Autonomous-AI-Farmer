/* ===========================================
   ROUTER — Hash-based SPA Router
   =========================================== */

const routes = {};
let currentCleanup = null;

export function registerRoute(path, handler) {
  routes[path] = handler;
}

export function navigate(path) {
  window.location.hash = path;
}

export function getCurrentRoute() {
  const hash = window.location.hash.slice(1) || '/';
  return hash;
}

export function getRouteParams() {
  const hash = getCurrentRoute();
  const parts = hash.split('/').filter(Boolean);
  return parts;
}

function matchRoute(hash) {
  // Exact match first
  if (routes[hash]) return { handler: routes[hash], params: {} };

  // Pattern match (e.g., /agent/:id)
  for (const [pattern, handler] of Object.entries(routes)) {
    const patternParts = pattern.split('/').filter(Boolean);
    const hashParts = hash.split('/').filter(Boolean);

    if (patternParts.length !== hashParts.length) continue;

    const params = {};
    let match = true;

    for (let i = 0; i < patternParts.length; i++) {
      if (patternParts[i].startsWith(':')) {
        params[patternParts[i].slice(1)] = hashParts[i];
      } else if (patternParts[i] !== hashParts[i]) {
        match = false;
        break;
      }
    }

    if (match) return { handler, params };
  }

  return null;
}

export async function handleRoute() {
  const hash = getCurrentRoute();
  const app = document.getElementById('app');

  // Run cleanup for previous page
  if (currentCleanup && typeof currentCleanup === 'function') {
    currentCleanup();
    currentCleanup = null;
  }

  const result = matchRoute(hash);

  if (result) {
    const { handler, params } = result;
    const pageResult = await handler(params);

    if (typeof pageResult === 'string') {
      app.innerHTML = pageResult;
    } else if (pageResult && pageResult.html) {
      app.innerHTML = pageResult.html;
      if (pageResult.init) {
        currentCleanup = pageResult.init();
      }
    }
  } else {
    // Fallback to home
    navigate('/');
  }
}

export function initRouter() {
  window.addEventListener('hashchange', handleRoute);

  // Handle clicks on internal links
  document.addEventListener('click', (e) => {
    const link = e.target.closest('a[href^="#"]');
    if (link) {
      e.preventDefault();
      const path = link.getAttribute('href').slice(1);
      navigate(path);
    }
  });

  // Initial route
  handleRoute();
}
