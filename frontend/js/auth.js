// auth.js
const MASTER_PIN = "admin123";

document.addEventListener('DOMContentLoaded', () => {
    // Inject the authentication modal into the DOM if it doesn't exist
    if (!document.getElementById('auth-modal')) {
        const modalHtml = `
            <div class="auth-overlay" id="auth-modal" style="display: none;">
                <div class="auth-card">
                    <h3 class="auth-title">Landlord Access</h3>
                    <p class="auth-desc">Please enter the master PIN to access this section.</p>
                    <div class="form-group" style="margin-bottom: 1rem;">
                        <input type="password" id="auth-pin-input" placeholder="Enter PIN" style="text-align: center; font-size: 1.2rem; letter-spacing: 5px;">
                    </div>
                    <p id="auth-error" style="color: #ef4444; font-size: 0.85rem; margin-bottom: 1rem; display: none; text-align: center;">Incorrect PIN. Please try again.</p>
                    <div class="modal-buttons" style="display: flex; justify-content: center; gap: 1rem;">
                        <button class="btn-cancel" id="auth-cancel-btn">Cancel</button>
                        <button class="btn-submit" id="auth-submit-btn">Unlock</button>
                    </div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHtml);

        // Bind events
        document.getElementById('auth-cancel-btn').addEventListener('click', closeAuthModal);
        document.getElementById('auth-submit-btn').addEventListener('click', checkPin);
        document.getElementById('auth-pin-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') checkPin();
        });
    }

    // Intercept clicks on Landlord Section links
    const landlordLinks = document.querySelectorAll('a[href="ExportPage.html"], a[href="announcements.html"]');
    
    landlordLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Check if already authenticated
            if (sessionStorage.getItem('isLandlord') === 'true') {
                return; // Let navigation proceed naturally
            }

            // Not authenticated, block navigation and show modal
            e.preventDefault();
            window.pendingAuthHref = this.getAttribute('href'); // Store where they wanted to go
            openAuthModal();
        });
    });
});

function openAuthModal() {
    const modal = document.getElementById('auth-modal');
    const input = document.getElementById('auth-pin-input');
    const error = document.getElementById('auth-error');
    
    input.value = '';
    error.style.display = 'none';
    modal.style.display = 'flex';
    setTimeout(() => input.focus(), 100);
}

function closeAuthModal() {
    document.getElementById('auth-modal').style.display = 'none';
    window.pendingAuthHref = null;
}

function checkPin() {
    const input = document.getElementById('auth-pin-input');
    const error = document.getElementById('auth-error');
    
    if (input.value === MASTER_PIN) {
        // Success
        sessionStorage.setItem('isLandlord', 'true');
        closeAuthModal();
        if (window.pendingAuthHref) {
            window.location.href = window.pendingAuthHref;
        }
    } else {
        // Failure
        error.style.display = 'block';
        input.value = '';
        input.focus();
    }
}
