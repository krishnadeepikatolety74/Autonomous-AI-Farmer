/* ===========================================
   WEATHER ANIMATION — Clouds, Leaves, Sunlight
   =========================================== */

let leafInterval = null;
let animationFrame = null;

export function createWeatherEnvironment() {
  return `
    <div class="weather-env" id="weather-env">
      <!-- Clouds -->
      <div class="cloud cloud-1">
        <div class="cloud-shape large"></div>
      </div>
      <div class="cloud cloud-2">
        <div class="cloud-shape"></div>
      </div>
      <div class="cloud cloud-3">
        <div class="cloud-shape small"></div>
      </div>
      <div class="cloud cloud-4">
        <div class="cloud-shape"></div>
      </div>

      <!-- Sunlight glow -->
      <div class="sunlight"></div>

      <!-- Leaves container -->
      <div id="leaves-container"></div>
    </div>
  `;
}

function createLeaf() {
  const container = document.getElementById('leaves-container');
  if (!container) return;

  const leaf = document.createElement('div');
  leaf.className = 'leaf';

  // Random leaf emoji
  const leaves = ['🍃', '🌿', '☘️', '🍂'];
  leaf.textContent = leaves[Math.floor(Math.random() * leaves.length)];

  // Random position and timing
  const startX = Math.random() * window.innerWidth;
  const duration = 12 + Math.random() * 15;
  const swayAmount = 30 + Math.random() * 60;
  const size = 14 + Math.random() * 10;

  leaf.style.left = `${startX}px`;
  leaf.style.top = '-20px';
  leaf.style.fontSize = `${size}px`;
  leaf.style.animation = `leaf-fall ${duration}s linear forwards`;

  container.appendChild(leaf);

  // Remove after animation
  setTimeout(() => {
    if (leaf.parentNode) {
      leaf.parentNode.removeChild(leaf);
    }
  }, duration * 1000);
}

export function startWeatherAnimations() {
  // Create leaves periodically
  leafInterval = setInterval(createLeaf, 3000);

  // Create a few initial leaves
  setTimeout(createLeaf, 500);
  setTimeout(createLeaf, 1500);
}

export function stopWeatherAnimations() {
  if (leafInterval) {
    clearInterval(leafInterval);
    leafInterval = null;
  }
  if (animationFrame) {
    cancelAnimationFrame(animationFrame);
    animationFrame = null;
  }
}

// Parallax effect on scroll
export function initParallax() {
  const handleScroll = () => {
    const env = document.getElementById('weather-env');
    if (!env) return;

    const scrollY = window.scrollY;
    const clouds = env.querySelectorAll('.cloud');

    clouds.forEach((cloud, i) => {
      const speed = 0.1 + (i * 0.05);
      cloud.style.transform = `translateY(${scrollY * speed}px)`;
    });
  };

  window.addEventListener('scroll', handleScroll, { passive: true });
  return () => window.removeEventListener('scroll', handleScroll);
}
