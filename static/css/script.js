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