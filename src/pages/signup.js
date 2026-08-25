/* ===========================================
   SIGN UP PAGE
   =========================================== */

export function renderSignUp() {
  const html = `
    <div class="split-layout page-transition">
      <!-- Left: Farm Image -->
      <div class="split-image">
        <img src="/images/signup-farm.png" alt="Farm Landscape" />
        <div style="position: absolute; inset: 0; background: linear-gradient(135deg, rgba(40, 89, 67, 0.15) 0%, transparent 100%);"></div>
      </div>

      <!-- Right: Sign Up Form -->
      <div class="split-form">
        <div class="form-container">
          <a href="#/" class="back-link">← Back to Home</a>

          <h2>Create Your<br>AI Farmer Account 🌿</h2>
          <p class="form-subtitle">Join the future of smart farming with AI.</p>

          <div class="form-fields">
            <div class="input-group">
              <label for="signup-name">Full Name</label>
              <input type="text" id="signup-name" class="input-field" placeholder="Enter your full name" />
            </div>

            <div class="input-group">
              <label for="signup-email">Email Address</label>
              <input type="email" id="signup-email" class="input-field" placeholder="Enter your email" />
            </div>

            <div class="input-group">
              <label for="signup-password">Password</label>
              <div class="input-password-wrapper">
                <input type="password" id="signup-password" class="input-field" placeholder="Create a password" />
                <button class="toggle-password" type="button" aria-label="Toggle password visibility" data-target="signup-password">👁</button>
              </div>
            </div>

            <div class="input-group">
              <label for="signup-confirm">Confirm Password</label>
              <div class="input-password-wrapper">
                <input type="password" id="signup-confirm" class="input-field" placeholder="Confirm your password" />
                <button class="toggle-password" type="button" aria-label="Toggle password visibility" data-target="signup-confirm">👁</button>
              </div>
            </div>

            <div class="checkbox-group">
              <input type="checkbox" id="signup-terms" />
              <label for="signup-terms">
                I agree to the <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a>
              </label>
            </div>

            <button class="btn btn-primary btn-lg" style="width: 100%; margin-top: 8px;" id="signup-btn">
              Sign Up
            </button>

            <p class="form-footer">
              Already have an account? <a href="#/signin">Sign In</a>
            </p>
          </div>
        </div>
      </div>
    </div>
  `;

  return {
    html,
    init: () => {
      // Toggle password visibility
      document.querySelectorAll('.toggle-password').forEach(btn => {
        btn.addEventListener('click', () => {
          const target = document.getElementById(btn.dataset.target);
          if (target) {
            target.type = target.type === 'password' ? 'text' : 'password';
            btn.textContent = target.type === 'password' ? '👁' : '👁‍🗨';
          }
        });
      });

      return () => {};
    }
  };
}
