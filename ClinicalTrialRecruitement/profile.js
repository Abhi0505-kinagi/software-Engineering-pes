const profileForm = document.querySelector('#profile-form');
const profileMessage = document.querySelector('#profile-message');
const cancelButton = document.querySelector('#cancel-button');
const initialValues = [...profileForm.elements].map((control) => ({
  control,
  value: control.value,
  checked: control.checked
}));

profileForm.addEventListener('submit', (event) => {
  event.preventDefault();

  if (!profileForm.checkValidity()) {
    profileForm.reportValidity();
    return;
  }

  const firstName = document.querySelector('#profile-first-name').value.trim();
  profileMessage.textContent = `Your profile changes are saved, ${firstName}.`;
});

cancelButton.addEventListener('click', () => {
  initialValues.forEach(({ control, value, checked }) => {
    control.value = value;
    control.checked = checked;
  });
  profileMessage.textContent = 'Your unsaved changes were cancelled.';
});
