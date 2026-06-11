document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const email = document.getElementById('email');
            const password = document.getElementById('password');
            const emailError = document.getElementById('emailError');
            const passwordError = document.getElementById('passwordError');
            let valid = true;

            emailError.style.display = 'none';
            passwordError.style.display = 'none';

            if (!email.value.includes('@')) {
                emailError.textContent = 'Please enter a valid email address';
                emailError.style.display = 'block';
                valid = false;
            }

            if (password.value.length < 4) {
                passwordError.textContent = 'Password must be at least 4 characters';
                passwordError.style.display = 'block';
                valid = false;
            }

            if (!valid) {
                e.preventDefault();
            }
        });
    }
});
