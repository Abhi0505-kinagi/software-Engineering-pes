const form = document.querySelector('#registration-form');
const message = document.querySelector('#form-message');

form.addEventListener('submit', (event) => {
  event.preventDefault();
  message.textContent = '';

  if (!form.checkValidity()) {
    form.reportValidity();
    return;
  }

  const password = document.querySelector('#password');
  if (password.value.length < 8) {
    password.setCustomValidity('Password must be at least 8 characters.');
    password.reportValidity();
    password.setCustomValidity('');
    return;
  }

  const firstName = document.querySelector('#first-name').value.trim();
  message.textContent = `Thanks, ${firstName}. Your profile is ready to explore.`;
  form.reset();
});
