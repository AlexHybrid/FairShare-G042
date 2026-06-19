// This file handles the basic frontend logic
// specifically switching between the Login and Signup forms on the same page

document.addEventListener('DOMContentLoaded', () => {
    // Get the HTML elements we need to interact with
    const loginSection = document.getElementById('login-section');
    const signupSection = document.getElementById('signup-section');
    const showSignupBtn = document.getElementById('show-signup');
    const showLoginBtn = document.getElementById('show-login');

    // Function to show the Signup form and hide the Login form
    if (showSignupBtn) {
        showSignupBtn.addEventListener('click', (e) => {
            e.preventDefault(); // Prevent the link from refreshing the page
            loginSection.classList.remove('active');
            signupSection.classList.add('active');
        });
    }

    // Function to show the Login form and hide the Signup form
    if (showLoginBtn) {
        showLoginBtn.addEventListener('click', (e) => {
            e.preventDefault(); // Prevent the link from refreshing the page
            signupSection.classList.remove('active');
            loginSection.classList.add('active');
        });
    }

    // Navbar Login button action: Switch to login form, scroll, and apply glow
    const navLoginBtn = document.getElementById('nav-login-btn');
    if (navLoginBtn) {
        navLoginBtn.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Switch view to login form if it is hidden
            if (signupSection && loginSection) {
                signupSection.classList.remove('active');
                loginSection.classList.add('active');
            }

            // Scroll to the auth container
            const authContainer = document.getElementById('auth-container');
            if (authContainer) {
                authContainer.scrollIntoView({ behavior: 'smooth' });
                
                // Add glow animation to the card
                const card = authContainer.querySelector('.card');
                if (card) {
                    card.classList.add('glow');
                    setTimeout(() => {
                        card.classList.remove('glow');
                    }, 2000);
                }
            }
        });
    }
});