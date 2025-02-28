document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('.toggle-password').forEach(icon => {
      icon.addEventListener('click', () => {
        const passwordInput = icon.previousElementSibling;
        
        if(passwordInput) { // Sicherheitscheck
          const type = passwordInput.type === 'password' ? 'text' : 'password';
          passwordInput.type = type;
          icon.classList.toggle('fa-eye-slash');
        }
      });
    });
  });