/* ===========================================
   DASHBOARD PAGE — Festival Planner
   =========================================== */

export function renderDashboard() {
  const today = new Date();

  // Festival date — Onam 2026 is 28 Aug 2026
  const festivalDate = new Date(2026, 7, 28); // Month is 0-indexed
  const diffTime = festivalDate.getTime() - today.getTime();
  const daysToGo = Math.max(0, Math.ceil(diffTime / (1000 * 60 * 60 * 24)));

  const festivalDateStr = festivalDate.toLocaleDateString('en-GB', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  });

  const html = `
    <div class="fp-dashboard-layout page-transition">
      <!-- ===== SIDEBAR ===== -->
      <aside class="fp-sidebar" id="fp-sidebar">
        <!-- Upcoming Festival Card -->
        <div class="fp-sidebar-festival-card">
          <div class="fp-festival-header">
            <span class="fp-festival-label">Upcoming Festival</span>
          </div>
          <div class="fp-festival-name">
            <span>Onam</span>
            <span class="fp-festival-emoji">🎋</span>
          </div>
          <div class="fp-festival-date-row">
            <span class="fp-festival-date-badge">${festivalDateStr}</span>
          </div>
          <div class="fp-festival-countdown">${daysToGo} Days to go!</div>

          <div class="fp-festival-image">
            <div class="fp-festival-img-placeholder">
              <div class="fp-onam-art">
                <span class="fp-onam-text">Happy</span>
                <span class="fp-onam-title">Onam</span>
                <div class="fp-onam-decoration">🌺🪷🌴🎉</div>
              </div>
            </div>
          </div>

          <div class="fp-festival-info">
            <div class="fp-info-item">
              <span class="fp-info-icon">📍</span>
              <span>Hyderabad, Telangana</span>
            </div>
            <div class="fp-info-item">
              <span class="fp-info-icon">👨‍👩‍👧‍👦</span>
              <span>Family Size: 4 Members</span>
            </div>
            <div class="fp-info-item">
              <span class="fp-info-icon">💰</span>
              <span>Budget: ₹15,000</span>
            </div>
            <div class="fp-info-item">
              <span class="fp-info-icon">🌐</span>
              <span>Language: English</span>
            </div>
          </div>

          <button class="fp-view-plan-btn" onclick="window.location.hash='#/plan'">View Full Plan</button>
        </div>

        <!-- Navigation -->
        <nav class="fp-sidebar-nav">
          <a href="#/dashboard" class="fp-nav-item active" data-page="dashboard">
            <span class="fp-nav-icon">📊</span>
            <span>Dashboard</span>
          </a>
          <a href="#/plan" class="fp-nav-item" data-page="plan">
            <span class="fp-nav-icon">📋</span>
            <span>My Plan</span>
          </a>
          <a href="#/calendar" class="fp-nav-item" data-page="calendar">
            <span class="fp-nav-icon">📅</span>
            <span>Festival Calendar</span>
          </a>
          <a href="#/shopping" class="fp-nav-item" data-page="shopping">
            <span class="fp-nav-icon">🛒</span>
            <span>Shopping List</span>
          </a>
          <a href="#/budget" class="fp-nav-item" data-page="budget">
            <span class="fp-nav-icon">💰</span>
            <span>Budget Planner</span>
          </a>
          <a href="#/recipes" class="fp-nav-item" data-page="recipes">
            <span class="fp-nav-icon">🍽️</span>
            <span>Recipes</span>
          </a>
          <a href="#/rituals" class="fp-nav-item" data-page="rituals">
            <span class="fp-nav-icon">🙏</span>
            <span>Rituals & Puja</span>
          </a>
          <a href="#/invitations" class="fp-nav-item" data-page="invitations">
            <span class="fp-nav-icon">💌</span>
            <span>Invitations</span>
          </a>
          <a href="#/stores" class="fp-nav-item" data-page="stores">
            <span class="fp-nav-icon">🏪</span>
            <span>Nearby Stores</span>
          </a>
          <a href="#/reports" class="fp-nav-item" data-page="reports">
            <span class="fp-nav-icon">📊</span>
            <span>Reports</span>
          </a>
          <a href="#/settings" class="fp-nav-item" data-page="settings">
            <span class="fp-nav-icon">⚙️</span>
            <span>Settings</span>
          </a>
        </nav>
      </aside>
      <div class="fp-sidebar-overlay" id="fp-sidebar-overlay"></div>

      <!-- ===== MAIN CONTENT ===== -->
      <main class="fp-main-content">
        <!-- Header -->
        <header class="fp-header">
          <div class="fp-header-left">
            <span class="fp-header-tag">YOUR PERSONAL FESTIVAL PLANNER</span>
            <h1 class="fp-header-title">Welcome back, kookie! 👋</h1>
            <p class="fp-header-subtitle">Let's plan your perfect festival</p>
          </div>
          <div class="fp-header-right">
            <div class="fp-lang-selector">
              <span>🌐</span>
              <span>English</span>
              <span class="fp-chevron">▾</span>
            </div>
            <button class="fp-header-icon-btn" aria-label="Notifications">
              <span>🔔</span>
              <span class="fp-notif-dot"></span>
            </button>
            <div class="fp-user-pill">
              <div class="fp-user-avatar-sm">K</div>
              <span>kookie</span>
              <span class="fp-chevron">▾</span>
            </div>
          </div>
        </header>

        <!-- ===== STAT CARDS ROW ===== -->
        <div class="fp-stats-row">
          <div class="fp-stat-card fp-animate-in" style="--delay: 0.05s">
            <div class="fp-stat-icon" style="background: #FFF3E0; color: #FF9800;">🍴</div>
            <div class="fp-stat-info">
              <span class="fp-stat-label">Recipes</span>
              <span class="fp-stat-value">5</span>
              <span class="fp-stat-desc">Generated recipes</span>
              <a class="fp-stat-link" href="#/recipes">View Recipes →</a>
            </div>
          </div>
          <div class="fp-stat-card fp-animate-in" style="--delay: 0.1s">
            <div class="fp-stat-icon" style="background: #F3E5F5; color: #9C27B0;">🙏</div>
            <div class="fp-stat-info">
              <span class="fp-stat-label">Rituals & Puja</span>
              <span class="fp-stat-value">5</span>
              <span class="fp-stat-desc">Generated rituals</span>
              <a class="fp-stat-link" href="#/rituals">View Guide →</a>
            </div>
          </div>
          <div class="fp-stat-card fp-animate-in" style="--delay: 0.15s">
            <div class="fp-stat-icon" style="background: #E8F5E9; color: #4CAF50;">🛒</div>
            <div class="fp-stat-info">
              <span class="fp-stat-label">Shopping Items</span>
              <span class="fp-stat-value">15</span>
              <span class="fp-stat-desc">Generated items</span>
              <a class="fp-stat-link" href="#/shopping">View List →</a>
            </div>
          </div>
          <div class="fp-stat-card fp-animate-in" style="--delay: 0.2s">
            <div class="fp-stat-icon" style="background: #E3F2FD; color: #2196F3;">💌</div>
            <div class="fp-stat-info">
              <span class="fp-stat-label">Invitations</span>
              <span class="fp-stat-value">1</span>
              <span class="fp-stat-desc">Content items</span>
              <a class="fp-stat-link" href="#/invitations">View Invites →</a>
            </div>
          </div>
          <div class="fp-stat-card fp-animate-in" style="--delay: 0.25s">
            <div class="fp-stat-icon" style="background: #FFF8E1; color: #FFC107;">📅</div>
            <div class="fp-stat-info">
              <span class="fp-stat-label">Timeline Tasks</span>
              <span class="fp-stat-value">3</span>
              <span class="fp-stat-desc">Preparation tasks</span>
              <a class="fp-stat-link" href="#/calendar">View Timeline →</a>
            </div>
          </div>
          <div class="fp-stat-card fp-animate-in" style="--delay: 0.3s">
            <div class="fp-stat-icon" style="background: #E8EAF6; color: #5C6BC0;">💳</div>
            <div class="fp-stat-info">
              <span class="fp-stat-label">Budget</span>
              <span class="fp-stat-value">₹15,000</span>
              <span class="fp-stat-desc">Planned spending</span>
              <a class="fp-stat-link" href="#/budget">View Budget →</a>
            </div>
          </div>
        </div>

        <!-- ===== ROW 2: Recipe + Shopping ===== -->
        <div class="fp-grid-2col">
          <!-- Recipe Distribution -->
          <div class="fp-card fp-animate-in" style="--delay: 0.35s">
            <div class="fp-card-header">
              <h3>Recipe distribution</h3>
            </div>
            <div class="fp-card-subheader">
              <span>🍽️ Recipes by Category</span>
            </div>
            <div class="fp-recipe-chart-area">
              <div class="fp-donut-container">
                <canvas id="fp-recipe-donut" width="180" height="180"></canvas>
                <div class="fp-donut-center-label">
                  <span class="fp-donut-number">5</span>
                  <span class="fp-donut-text">Total<br>Recipes</span>
                </div>
              </div>
              <div class="fp-recipe-legend">
                <div class="fp-legend-item"><span class="fp-legend-dot" style="background:#6366F1;"></span> Main Course <strong>2</strong></div>
                <div class="fp-legend-item"><span class="fp-legend-dot" style="background:#F97316;"></span> Dessert <strong>1</strong></div>
                <div class="fp-legend-item"><span class="fp-legend-dot" style="background:#EC4899;"></span> Sweet <strong>1</strong></div>
                <div class="fp-legend-item"><span class="fp-legend-dot" style="background:#22C55E;"></span> Drink <strong>1</strong></div>
              </div>
            </div>
          </div>

          <!-- Shopping List Overview -->
          <div class="fp-card fp-animate-in" style="--delay: 0.4s">
            <div class="fp-card-header">
              <h3>Shopping List Overview</h3>
            </div>
            <div class="fp-card-subheader">
              <span>🛍️ Purchased vs Pending</span>
            </div>
            <div class="fp-shopping-overview">
              <div class="fp-shopping-donut-area">
                <canvas id="fp-shopping-donut" width="140" height="140"></canvas>
                <div class="fp-donut-center-label fp-donut-center-sm">
                  <span class="fp-donut-number">15</span>
                  <span class="fp-donut-text">Total<br>Items</span>
                </div>
              </div>
              <div class="fp-shopping-bars">
                <div class="fp-bar-row">
                  <span class="fp-bar-label">Purchased</span>
                  <div class="fp-progress-track">
                    <div class="fp-progress-fill" style="width: 0%; background: #22C55E;"></div>
                  </div>
                  <span class="fp-bar-value">0</span>
                </div>
                <div class="fp-bar-row">
                  <span class="fp-bar-label">Pending</span>
                  <div class="fp-progress-track">
                    <div class="fp-progress-fill" style="width: 100%; background: #6366F1;"></div>
                  </div>
                  <span class="fp-bar-value">15</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ===== ROW 3: Budget + Timeline ===== -->
        <div class="fp-grid-2col">
          <!-- Budget Breakdown -->
          <div class="fp-card fp-animate-in" style="--delay: 0.45s">
            <div class="fp-card-header">
              <h3>Budget Breakdown</h3>
              <span class="fp-card-header-value">₹15,000</span>
            </div>
            <div class="fp-card-subheader">
              <span>💰 Budget by Category</span>
            </div>
            <div class="fp-budget-bars">
              <div class="fp-budget-row">
                <span class="fp-budget-label">Food</span>
                <div class="fp-budget-bar-track">
                  <div class="fp-budget-bar-fill" style="width: 40%; background: #F97316;"></div>
                </div>
                <span class="fp-budget-amount">₹0</span>
              </div>
              <div class="fp-budget-row">
                <span class="fp-budget-label">Shopping</span>
                <div class="fp-budget-bar-track">
                  <div class="fp-budget-bar-fill" style="width: 25%; background: #EF4444;"></div>
                </div>
                <span class="fp-budget-amount">₹0</span>
              </div>
              <div class="fp-budget-row">
                <span class="fp-budget-label">Decorations</span>
                <div class="fp-budget-bar-track">
                  <div class="fp-budget-bar-fill" style="width: 30%; background: #3B82F6;"></div>
                </div>
                <span class="fp-budget-amount">₹0</span>
              </div>
              <div class="fp-budget-row">
                <span class="fp-budget-label">Puja</span>
                <div class="fp-budget-bar-track">
                  <div class="fp-budget-bar-fill" style="width: 20%; background: #22C55E;"></div>
                </div>
                <span class="fp-budget-amount">₹0</span>
              </div>
              <div class="fp-budget-row">
                <span class="fp-budget-label">Other</span>
                <div class="fp-budget-bar-track">
                  <div class="fp-budget-bar-fill" style="width: 15%; background: #6366F1;"></div>
                </div>
                <span class="fp-budget-amount">₹0</span>
              </div>
            </div>
          </div>

          <!-- Preparation Timeline -->
          <div class="fp-card fp-animate-in" style="--delay: 0.5s">
            <div class="fp-card-header">
              <h3>Preparation Timeline</h3>
              <span class="fp-card-header-value fp-timeline-count">3</span>
            </div>
            <div class="fp-card-subheader">
              <span>📊 Timeline Progress</span>
            </div>
            <div class="fp-timeline-chart-area">
              <canvas id="fp-timeline-chart" width="480" height="200"></canvas>
            </div>
          </div>
        </div>

        <!-- ===== ROW 4: Tasks + Activity ===== -->
        <div class="fp-grid-2col">
          <!-- Upcoming Tasks -->
          <div class="fp-card fp-animate-in" style="--delay: 0.55s">
            <div class="fp-card-header">
              <h3>Upcoming Tasks</h3>
            </div>
            <div class="fp-tasks-list">
              <div class="fp-task-item">
                <div class="fp-task-icon" style="background: #E8F5E9;">🛒</div>
                <div class="fp-task-info">
                  <span class="fp-task-name">Buy flowers and decorations</span>
                </div>
                <span class="fp-task-date">24 Aug 2026</span>
                <span class="fp-task-time">🕐 10:00 AM</span>
                <span class="fp-task-badge fp-badge-shopping">Shopping</span>
              </div>
              <div class="fp-task-item">
                <div class="fp-task-icon" style="background: #FFF3E0;">🍳</div>
                <div class="fp-task-info">
                  <span class="fp-task-name">Prepare Onam Sadhya Ingredients</span>
                </div>
                <span class="fp-task-date">25 Aug 2026</span>
                <span class="fp-task-time">🕐 04:00 PM</span>
                <span class="fp-task-badge fp-badge-cooking">Cooking</span>
              </div>
              <div class="fp-task-item">
                <div class="fp-task-icon" style="background: #F3E5F5;">🙏</div>
                <div class="fp-task-info">
                  <span class="fp-task-name">Onam Pooja & Arrangements</span>
                </div>
                <span class="fp-task-date">26 Aug 2026</span>
                <span class="fp-task-time">🕐 07:00 AM</span>
                <span class="fp-task-badge fp-badge-puja">Puja</span>
              </div>
            </div>
            <a class="fp-view-more-link" href="#/calendar">View Full Timeline →</a>
          </div>

          <!-- Recent Activity -->
          <div class="fp-card fp-animate-in" style="--delay: 0.6s">
            <div class="fp-card-header">
              <h3>Recent Activity</h3>
            </div>
            <div class="fp-activity-list">
              <div class="fp-activity-item">
                <div class="fp-activity-dot fp-dot-green">✓</div>
                <div class="fp-activity-info">
                  <span>Shopping item "Banana Leaves" marked as purchased</span>
                </div>
                <span class="fp-activity-time">2 mins ago</span>
              </div>
              <div class="fp-activity-item">
                <div class="fp-activity-dot fp-dot-purple">📋</div>
                <div class="fp-activity-info">
                  <span>Recipe "Avial" added to plan</span>
                </div>
                <span class="fp-activity-time">15 mins ago</span>
              </div>
              <div class="fp-activity-item">
                <div class="fp-activity-dot fp-dot-orange">💌</div>
                <div class="fp-activity-info">
                  <span>Invitation created for family members</span>
                </div>
                <span class="fp-activity-time">1 hour ago</span>
              </div>
              <div class="fp-activity-item">
                <div class="fp-activity-dot fp-dot-blue">💰</div>
                <div class="fp-activity-info">
                  <span>Budget updated: Added ₹3,000 to Decorations</span>
                </div>
                <span class="fp-activity-time">2 hours ago</span>
              </div>
            </div>
            <a class="fp-view-more-link" href="#/activity">View All Activity →</a>
          </div>
        </div>

      </main>
    </div>

    <style>
      /* ============================================================
         FESTIVAL PLANNER DASHBOARD — Scoped Styles
         ============================================================ */

      /* --- Layout --- */
      .fp-dashboard-layout {
        display: flex;
        min-height: 100vh;
        background: #F8F9FE;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      }

      /* --- Sidebar --- */
      .fp-sidebar {
        position: fixed;
        top: 0;
        left: 0;
        width: 280px;
        height: 100vh;
        background: #FFFFFF;
        border-right: 1px solid #F0F0F5;
        display: flex;
        flex-direction: column;
        padding: 0;
        z-index: 100;
        overflow-y: auto;
        scrollbar-width: thin;
      }

      .fp-sidebar::-webkit-scrollbar {
        width: 4px;
      }
      .fp-sidebar::-webkit-scrollbar-thumb {
        background: #DDD;
        border-radius: 4px;
      }

      /* Festival Card in Sidebar */
      .fp-sidebar-festival-card {
        padding: 20px 18px 16px;
        border-bottom: 1px solid #F0F0F5;
      }

      .fp-festival-header {
        margin-bottom: 4px;
      }

      .fp-festival-label {
        font-size: 11px;
        font-weight: 600;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.5px;
      }

      .fp-festival-name {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 22px;
        font-weight: 800;
        color: #1A1A2E;
        margin: 4px 0 8px;
      }

      .fp-festival-emoji {
        font-size: 20px;
      }

      .fp-festival-date-row {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 4px;
      }

      .fp-festival-date-badge {
        background: #EEF0FF;
        color: #6C5CE7;
        font-size: 11px;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 20px;
      }

      .fp-festival-countdown {
        font-size: 13px;
        font-weight: 700;
        color: #E74C3C;
        margin-bottom: 12px;
      }

      .fp-festival-image {
        border-radius: 14px;
        overflow: hidden;
        margin-bottom: 14px;
        height: 130px;
        position: relative;
      }

      .fp-festival-img-placeholder {
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #FFD93D 0%, #FF6B6B 40%, #6C5CE7 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
      }

      .fp-festival-img-placeholder::before {
        content: '';
        position: absolute;
        top: -20px;
        right: -20px;
        width: 100px;
        height: 100px;
        background: rgba(255,255,255,0.15);
        border-radius: 50%;
      }

      .fp-festival-img-placeholder::after {
        content: '';
        position: absolute;
        bottom: -30px;
        left: -10px;
        width: 80px;
        height: 80px;
        background: rgba(255,255,255,0.1);
        border-radius: 50%;
      }

      .fp-onam-art {
        text-align: center;
        color: white;
        z-index: 2;
        position: relative;
      }

      .fp-onam-text {
        display: block;
        font-size: 14px;
        font-weight: 600;
        opacity: 0.9;
        text-shadow: 0 1px 4px rgba(0,0,0,0.2);
      }

      .fp-onam-title {
        display: block;
        font-size: 32px;
        font-weight: 800;
        letter-spacing: 1px;
        text-shadow: 0 2px 8px rgba(0,0,0,0.2);
        font-style: italic;
      }

      .fp-onam-decoration {
        margin-top: 4px;
        font-size: 18px;
        letter-spacing: 4px;
      }

      .fp-festival-info {
        display: flex;
        flex-direction: column;
        gap: 6px;
        margin-bottom: 14px;
      }

      .fp-info-item {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 12px;
        color: #555;
      }

      .fp-info-icon {
        width: 18px;
        text-align: center;
        font-size: 13px;
      }

      .fp-view-plan-btn {
        width: 100%;
        padding: 10px 0;
        background: linear-gradient(135deg, #6C5CE7, #A855F7);
        color: white;
        border: none;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s ease;
        letter-spacing: 0.3px;
      }

      .fp-view-plan-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 16px rgba(108, 92, 231, 0.35);
      }

      /* Sidebar Nav */
      .fp-sidebar-nav {
        padding: 12px 12px 20px;
        display: flex;
        flex-direction: column;
        gap: 2px;
        flex: 1;
      }

      .fp-nav-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 9px 14px;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 500;
        color: #666;
        transition: all 0.2s ease;
        text-decoration: none;
        cursor: pointer;
      }

      .fp-nav-item:hover {
        background: #F5F3FF;
        color: #6C5CE7;
      }

      .fp-nav-item.active {
        background: #6C5CE7;
        color: white;
        font-weight: 600;
      }

      .fp-nav-icon {
        width: 20px;
        text-align: center;
        font-size: 15px;
      }

      .fp-sidebar-overlay {
        display: none;
      }

      /* --- Main Content --- */
      .fp-main-content {
        margin-left: 280px;
        flex: 1;
        padding: 28px 32px 40px;
        min-height: 100vh;
        background: #F8F9FE;
      }

      /* --- Header --- */
      .fp-header {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        margin-bottom: 28px;
      }

      .fp-header-tag {
        display: inline-block;
        font-size: 11px;
        font-weight: 700;
        color: #E74C3C;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 4px;
      }

      .fp-header-title {
        font-size: 26px;
        font-weight: 800;
        color: #1A1A2E;
        margin: 0 0 4px;
        letter-spacing: -0.5px;
      }

      .fp-header-subtitle {
        font-size: 14px;
        color: #888;
        margin: 0;
        font-weight: 400;
      }

      .fp-header-right {
        display: flex;
        align-items: center;
        gap: 12px;
      }

      .fp-lang-selector {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 7px 14px;
        background: white;
        border: 1px solid #E8E8F0;
        border-radius: 22px;
        font-size: 13px;
        font-weight: 500;
        color: #333;
        cursor: pointer;
        transition: all 0.2s ease;
      }

      .fp-lang-selector:hover {
        border-color: #6C5CE7;
      }

      .fp-chevron {
        font-size: 10px;
        color: #999;
      }

      .fp-header-icon-btn {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: white;
        border: 1px solid #E8E8F0;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        position: relative;
        font-size: 16px;
        transition: all 0.2s ease;
      }

      .fp-header-icon-btn:hover {
        border-color: #6C5CE7;
        background: #F5F3FF;
      }

      .fp-notif-dot {
        position: absolute;
        top: 6px;
        right: 6px;
        width: 8px;
        height: 8px;
        background: #E74C3C;
        border-radius: 50%;
        border: 2px solid white;
      }

      .fp-user-pill {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 5px 14px 5px 5px;
        background: white;
        border: 1px solid #E8E8F0;
        border-radius: 26px;
        font-size: 13px;
        font-weight: 500;
        color: #333;
        cursor: pointer;
        transition: all 0.2s ease;
      }

      .fp-user-pill:hover {
        border-color: #6C5CE7;
      }

      .fp-user-avatar-sm {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6C5CE7, #A855F7);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 13px;
      }

      /* --- Stat Cards Row --- */
      .fp-stats-row {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 16px;
        margin-bottom: 24px;
      }

      .fp-stat-card {
        background: white;
        border-radius: 16px;
        padding: 18px 16px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        border: 1px solid #F0F0F5;
        display: flex;
        flex-direction: column;
        gap: 10px;
        transition: all 0.3s ease;
        animation: fp-fadeInUp 0.5s ease forwards;
        animation-delay: var(--delay, 0s);
        opacity: 0;
      }

      .fp-stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 28px rgba(108, 92, 231, 0.12);
        border-color: rgba(108, 92, 231, 0.2);
      }

      .fp-stat-icon {
        width: 42px;
        height: 42px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
      }

      .fp-stat-info {
        display: flex;
        flex-direction: column;
      }

      .fp-stat-label {
        font-size: 12px;
        font-weight: 600;
        color: #888;
      }

      .fp-stat-value {
        font-size: 24px;
        font-weight: 800;
        color: #1A1A2E;
        letter-spacing: -0.5px;
      }

      .fp-stat-desc {
        font-size: 11px;
        color: #AAA;
        margin-top: 1px;
      }

      .fp-stat-link {
        font-size: 11px;
        font-weight: 600;
        color: #6C5CE7;
        text-decoration: none;
        margin-top: 4px;
        transition: color 0.2s;
      }

      .fp-stat-link:hover {
        color: #A855F7;
      }

      /* --- Cards --- */
      .fp-grid-2col {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin-bottom: 20px;
      }

      .fp-card {
        background: white;
        border-radius: 18px;
        padding: 22px 24px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        border: 1px solid #F0F0F5;
        transition: all 0.3s ease;
        animation: fp-fadeInUp 0.5s ease forwards;
        animation-delay: var(--delay, 0s);
        opacity: 0;
      }

      .fp-card:hover {
        box-shadow: 0 6px 24px rgba(108, 92, 231, 0.1);
      }

      .fp-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 4px;
      }

      .fp-card-header h3 {
        font-size: 16px;
        font-weight: 700;
        color: #1A1A2E;
        margin: 0;
      }

      .fp-card-header-value {
        font-size: 22px;
        font-weight: 800;
        color: #1A1A2E;
      }

      .fp-card-subheader {
        font-size: 12px;
        color: #888;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 6px;
      }

      /* --- Recipe Donut --- */
      .fp-recipe-chart-area {
        display: flex;
        align-items: center;
        gap: 28px;
      }

      .fp-donut-container {
        position: relative;
        width: 180px;
        height: 180px;
        flex-shrink: 0;
      }

      .fp-donut-center-label {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
        pointer-events: none;
      }

      .fp-donut-number {
        display: block;
        font-size: 28px;
        font-weight: 800;
        color: #1A1A2E;
        line-height: 1;
      }

      .fp-donut-text {
        display: block;
        font-size: 11px;
        color: #888;
        line-height: 1.3;
        margin-top: 2px;
      }

      .fp-donut-center-sm .fp-donut-number {
        font-size: 22px;
      }

      .fp-recipe-legend {
        display: flex;
        flex-direction: column;
        gap: 10px;
      }

      .fp-legend-item {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 13px;
        color: #555;
      }

      .fp-legend-item strong {
        margin-left: auto;
        color: #1A1A2E;
        font-weight: 700;
        min-width: 16px;
        text-align: right;
      }

      .fp-legend-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        flex-shrink: 0;
      }

      /* --- Shopping Overview --- */
      .fp-shopping-overview {
        display: flex;
        align-items: center;
        gap: 32px;
      }

      .fp-shopping-donut-area {
        position: relative;
        width: 140px;
        height: 140px;
        flex-shrink: 0;
      }

      .fp-shopping-bars {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 16px;
      }

      .fp-bar-row {
        display: flex;
        align-items: center;
        gap: 12px;
      }

      .fp-bar-label {
        font-size: 12px;
        color: #555;
        min-width: 72px;
        font-weight: 500;
      }

      .fp-progress-track {
        flex: 1;
        height: 10px;
        background: #F0F0F5;
        border-radius: 10px;
        overflow: hidden;
      }

      .fp-progress-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 1s ease;
      }

      .fp-bar-value {
        font-size: 14px;
        font-weight: 700;
        color: #1A1A2E;
        min-width: 24px;
        text-align: right;
      }

      /* --- Budget Breakdown --- */
      .fp-budget-bars {
        display: flex;
        flex-direction: column;
        gap: 14px;
      }

      .fp-budget-row {
        display: flex;
        align-items: center;
        gap: 12px;
      }

      .fp-budget-label {
        font-size: 13px;
        color: #555;
        min-width: 90px;
        font-weight: 500;
      }

      .fp-budget-bar-track {
        flex: 1;
        height: 10px;
        background: #F0F0F5;
        border-radius: 10px;
        overflow: hidden;
      }

      .fp-budget-bar-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 1s ease;
      }

      .fp-budget-amount {
        font-size: 13px;
        font-weight: 600;
        color: #888;
        min-width: 40px;
        text-align: right;
      }

      /* --- Timeline Chart --- */
      .fp-timeline-count {
        background: #F3E5F5;
        color: #9C27B0;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 16px;
        font-weight: 800;
      }

      .fp-timeline-chart-area {
        width: 100%;
        height: 200px;
        position: relative;
      }

      .fp-timeline-chart-area canvas {
        width: 100% !important;
        height: 100% !important;
      }

      /* --- Tasks --- */
      .fp-tasks-list {
        display: flex;
        flex-direction: column;
        gap: 12px;
        margin-bottom: 14px;
      }

      .fp-task-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 12px;
        border-radius: 12px;
        transition: background 0.2s ease;
      }

      .fp-task-item:hover {
        background: #FAFAFE;
      }

      .fp-task-icon {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        flex-shrink: 0;
      }

      .fp-task-info {
        flex: 1;
        min-width: 0;
      }

      .fp-task-name {
        font-size: 13px;
        font-weight: 600;
        color: #1A1A2E;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        display: block;
      }

      .fp-task-date {
        font-size: 11px;
        color: #888;
        white-space: nowrap;
      }

      .fp-task-time {
        font-size: 11px;
        color: #888;
        white-space: nowrap;
      }

      .fp-task-badge {
        font-size: 10px;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 20px;
        white-space: nowrap;
        text-transform: capitalize;
      }

      .fp-badge-shopping {
        background: #E8F5E9;
        color: #2E7D32;
      }

      .fp-badge-cooking {
        background: #FFF3E0;
        color: #E65100;
      }

      .fp-badge-puja {
        background: #F3E5F5;
        color: #7B1FA2;
      }

      .fp-view-more-link {
        display: inline-flex;
        align-items: center;
        font-size: 13px;
        font-weight: 600;
        color: #6C5CE7;
        text-decoration: none;
        transition: color 0.2s;
      }

      .fp-view-more-link:hover {
        color: #A855F7;
      }

      /* --- Activity --- */
      .fp-activity-list {
        display: flex;
        flex-direction: column;
        gap: 14px;
        margin-bottom: 14px;
      }

      .fp-activity-item {
        display: flex;
        align-items: flex-start;
        gap: 12px;
      }

      .fp-activity-dot {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        flex-shrink: 0;
        font-weight: 700;
      }

      .fp-dot-green {
        background: #E8F5E9;
        color: #2E7D32;
      }

      .fp-dot-purple {
        background: #F3E5F5;
        color: #7B1FA2;
      }

      .fp-dot-orange {
        background: #FFF3E0;
        color: #E65100;
      }

      .fp-dot-blue {
        background: #E3F2FD;
        color: #1565C0;
      }

      .fp-activity-info {
        flex: 1;
        font-size: 13px;
        color: #555;
        line-height: 1.5;
      }

      .fp-activity-time {
        font-size: 11px;
        color: #AAA;
        white-space: nowrap;
        flex-shrink: 0;
      }

      /* --- Animations --- */
      @keyframes fp-fadeInUp {
        from {
          opacity: 0;
          transform: translateY(18px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }

      .fp-animate-in {
        animation: fp-fadeInUp 0.5s ease forwards;
        animation-delay: var(--delay, 0s);
        opacity: 0;
      }

      /* --- Responsive --- */
      @media (max-width: 1400px) {
        .fp-stats-row {
          grid-template-columns: repeat(3, 1fr);
        }
      }

      @media (max-width: 1024px) {
        .fp-sidebar {
          transform: translateX(-100%);
          transition: transform 0.3s ease;
        }

        .fp-sidebar.open {
          transform: translateX(0);
        }

        .fp-sidebar-overlay.active {
          display: block;
          position: fixed;
          inset: 0;
          background: rgba(0,0,0,0.3);
          z-index: 99;
        }

        .fp-main-content {
          margin-left: 0;
          padding: 20px 16px;
        }

        .fp-grid-2col {
          grid-template-columns: 1fr;
        }

        .fp-stats-row {
          grid-template-columns: repeat(2, 1fr);
        }
      }

      @media (max-width: 640px) {
        .fp-stats-row {
          grid-template-columns: 1fr;
        }

        .fp-header {
          flex-direction: column;
          gap: 12px;
        }

        .fp-header-right {
          flex-wrap: wrap;
        }

        .fp-recipe-chart-area {
          flex-direction: column;
        }

        .fp-shopping-overview {
          flex-direction: column;
        }

        .fp-task-item {
          flex-wrap: wrap;
          gap: 6px;
        }
      }
    </style>
  `;

  return {
    html,
    init: () => {
      drawRecipeDonut();
      drawShoppingDonut();
      drawTimelineChart();

      // Sidebar overlay
      const overlay = document.getElementById('fp-sidebar-overlay');
      const sidebar = document.getElementById('fp-sidebar');
      if (overlay && sidebar) {
        overlay.addEventListener('click', () => {
          sidebar.classList.remove('open');
          overlay.classList.remove('active');
        });
      }

      return () => {};
    }
  };
}

/* =========================================
   CANVAS DRAWING FUNCTIONS
   ========================================= */

function drawRecipeDonut() {
  const canvas = document.getElementById('fp-recipe-donut');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  canvas.width = 180 * dpr;
  canvas.height = 180 * dpr;
  ctx.scale(dpr, dpr);

  const cx = 90, cy = 90, outerR = 80, innerR = 52;
  const data = [
    { value: 2, color: '#6366F1' },
    { value: 1, color: '#F97316' },
    { value: 1, color: '#EC4899' },
    { value: 1, color: '#22C55E' },
  ];
  const total = data.reduce((s, d) => s + d.value, 0);

  let startAngle = -Math.PI / 2;
  const gap = 0.04;

  data.forEach(segment => {
    const sweep = (segment.value / total) * (Math.PI * 2) - gap;
    ctx.beginPath();
    ctx.arc(cx, cy, outerR, startAngle, startAngle + sweep);
    ctx.arc(cx, cy, innerR, startAngle + sweep, startAngle, true);
    ctx.closePath();
    ctx.fillStyle = segment.color;
    ctx.fill();
    startAngle += sweep + gap;
  });
}

function drawShoppingDonut() {
  const canvas = document.getElementById('fp-shopping-donut');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  canvas.width = 140 * dpr;
  canvas.height = 140 * dpr;
  ctx.scale(dpr, dpr);

  const cx = 70, cy = 70, outerR = 62, innerR = 42;

  // Full circle — all pending (15 out of 15)
  ctx.beginPath();
  ctx.arc(cx, cy, outerR, 0, Math.PI * 2);
  ctx.arc(cx, cy, innerR, Math.PI * 2, 0, true);
  ctx.closePath();
  ctx.fillStyle = '#F97316';
  ctx.fill();
}

function drawTimelineChart() {
  const canvas = document.getElementById('fp-timeline-chart');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const W = canvas.parentElement.clientWidth || 480;
  const H = 200;
  canvas.width = W * dpr;
  canvas.height = H * dpr;
  canvas.style.width = W + 'px';
  canvas.style.height = H + 'px';
  ctx.scale(dpr, dpr);

  const labels = ['Preparation', 'Shopping', 'Cooking', 'Puja', 'Celebration'];
  const dataPoints = [1, 0.5, 0.3, 0.8, 3];

  const paddingLeft = 10;
  const paddingRight = 10;
  const paddingTop = 30;
  const paddingBottom = 30;
  const chartW = W - paddingLeft - paddingRight;
  const chartH = H - paddingTop - paddingBottom;

  const maxVal = Math.max(...dataPoints);
  const stepX = chartW / (labels.length - 1);

  // Grid lines
  ctx.strokeStyle = '#F0F0F5';
  ctx.lineWidth = 1;
  for (let i = 0; i <= 4; i++) {
    const y = paddingTop + (chartH / 4) * i;
    ctx.beginPath();
    ctx.moveTo(paddingLeft, y);
    ctx.lineTo(W - paddingRight, y);
    ctx.stroke();
  }

  // Data line
  const points = dataPoints.map((val, i) => ({
    x: paddingLeft + i * stepX,
    y: paddingTop + chartH - (val / maxVal) * chartH
  }));

  // Gradient fill
  const gradient = ctx.createLinearGradient(0, paddingTop, 0, H - paddingBottom);
  gradient.addColorStop(0, 'rgba(236, 72, 153, 0.15)');
  gradient.addColorStop(1, 'rgba(236, 72, 153, 0)');

  ctx.beginPath();
  ctx.moveTo(points[0].x, H - paddingBottom);
  points.forEach((p, i) => {
    if (i === 0) {
      ctx.lineTo(p.x, p.y);
    } else {
      const prev = points[i - 1];
      const cpx1 = prev.x + stepX * 0.4;
      const cpy1 = prev.y;
      const cpx2 = p.x - stepX * 0.4;
      const cpy2 = p.y;
      ctx.bezierCurveTo(cpx1, cpy1, cpx2, cpy2, p.x, p.y);
    }
  });
  ctx.lineTo(points[points.length - 1].x, H - paddingBottom);
  ctx.closePath();
  ctx.fillStyle = gradient;
  ctx.fill();

  // Line
  ctx.beginPath();
  points.forEach((p, i) => {
    if (i === 0) {
      ctx.moveTo(p.x, p.y);
    } else {
      const prev = points[i - 1];
      const cpx1 = prev.x + stepX * 0.4;
      const cpy1 = prev.y;
      const cpx2 = p.x - stepX * 0.4;
      const cpy2 = p.y;
      ctx.bezierCurveTo(cpx1, cpy1, cpx2, cpy2, p.x, p.y);
    }
  });
  ctx.strokeStyle = '#EC4899';
  ctx.lineWidth = 2.5;
  ctx.stroke();

  // Points
  points.forEach(p => {
    ctx.beginPath();
    ctx.arc(p.x, p.y, 4, 0, Math.PI * 2);
    ctx.fillStyle = '#EC4899';
    ctx.fill();
    ctx.beginPath();
    ctx.arc(p.x, p.y, 2, 0, Math.PI * 2);
    ctx.fillStyle = 'white';
    ctx.fill();
  });

  // Labels
  ctx.fillStyle = '#888';
  ctx.font = '11px Inter, sans-serif';
  ctx.textAlign = 'center';
  labels.forEach((label, i) => {
    ctx.fillText(label, paddingLeft + i * stepX, H - 8);
  });

  // Value label on last point
  const lastP = points[points.length - 1];
  ctx.fillStyle = '#1A1A2E';
  ctx.font = 'bold 14px Inter, sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('3', lastP.x, lastP.y - 12);
}
