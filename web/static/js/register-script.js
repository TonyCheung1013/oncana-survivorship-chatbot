// --- web/static/js/register-script.js ---

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('registration-form');
    const messageDiv = document.getElementById('registration-message');
  
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
  
      const user_id = document.getElementById('user_id').value.trim();
      const name = document.getElementById('name').value.trim();
      const password = document.getElementById('password').value.trim();
      const age = document.getElementById('age').value.trim();
      const cancer_type = document.getElementById('cancer_type').value;
      const custom_cancer = document.getElementById('custom_cancer').value.trim();
      const treatment_history = document.getElementById('treatment_history').value;
      const custom_treatment = document.getElementById('custom_treatment').value.trim();
  
      const finalCancerType = cancer_type === 'Other' ? custom_cancer : cancer_type;
      const finalTreatment = treatment_history === 'Other' ? custom_treatment : treatment_history;
  
      if (!user_id || !name || !password || !age || !finalCancerType || !finalTreatment) {
        showMessage('❗ All fields are required.', 'error');
        return;
      }
  
      try {
        const response = await fetch('/api/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user_id, name, password, age, cancer_type: finalCancerType, treatment_history: finalTreatment })
        });
        const data = await response.json();
        if (data.success) {
          showMessage('✅ Registration successful!', 'success');
          form.reset();
        } else {
          showMessage(`❗ ${data.message}`, 'error');
        }
      } catch (error) {
        showMessage('❗ Registration failed. Please try again later.', 'error');
      }
    });
  
    document.getElementById('cancer_type').addEventListener('change', (e) => {
      document.getElementById('custom_cancer').classList.toggle('hidden', e.target.value !== 'Other');
    });
  
    document.getElementById('treatment_history').addEventListener('change', (e) => {
      document.getElementById('custom_treatment').classList.toggle('hidden', e.target.value !== 'Other');
    });
  
    function showMessage(message, type) {
      messageDiv.textContent = message;
      messageDiv.className = 'message';
      if (type === 'error') {
        messageDiv.style.color = '#d86e34';
      } else {
        messageDiv.style.color = '#566862';
      }
    }
  });
  