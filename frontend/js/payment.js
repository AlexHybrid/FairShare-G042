const API_BASE = 'http://localhost:5000/api';

const tbody = document.getElementById('payment-table-body');
const paymentModal = document.getElementById('payment-modal');
const closePaymentModalBtn = document.getElementById('close-payment-modal');
const modalAmountEl = document.getElementById('modal-amount');
const modalPaymentMethodSelect = document.getElementById('modal-payment-method');
const confirmPaymentBtn = document.getElementById('confirm-payment-btn');

let currentPayingId = null;

// Theme room configuration for UI tags
const roomTheme = {
  'Room A': { tagClass: 'tag-green', color: '#fca5a5' },
  'Room B': { tagClass: 'tag-yellow', color: '#c084fc' },
  'Room C': { tagClass: 'tag-red', color: '#4f6bff' },
  'Room D': { tagClass: 'tag-blue', color: '#4ade80' },
  'Room E': { tagClass: 'tag-purple', color: '#f472b6' }
};

// Helper to get room tag HTML
function getRoomTagHTML(room) {
  const config = roomTheme[room] || { tagClass: 'tag-blue' };
  return `<span class="tag ${config.tagClass}">${room}</span>`;
}

document.addEventListener('DOMContentLoaded', () => {
  fetchPayments();
});

let allExpensesData = [];

async function fetchPayments() {
  try {
    const res = await fetch(`${API_BASE}/expenses`);
    if (!res.ok) throw new Error('Failed to fetch data');
    const data = await res.json();
    allExpensesData = data;
    renderTable(data);
  } catch (err) {
    console.error(err);
    tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: #ff6b6b; font-weight: 500;">Error loading data. Is the backend running?</td></tr>`;
  }
}

function renderTable(expenses) {
  tbody.innerHTML = '';

  if (expenses.length === 0) {
    tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: #94a3b8;">No expenses found.</td></tr>`;
    return;
  }

  expenses.forEach(exp => {
    const tr = document.createElement('tr');
    
    // Status Tag Styling
    let statusHTML = '';
    if (exp.status === 'Paid') {
      statusHTML = `<span class="tag tag-green">Paid</span>`;
    } else {
      statusHTML = `<span class="tag tag-yellow">Pending</span>`;
    }
    
    // Action Button
    let actionHTML = '';
    if (exp.status === 'Pending') {
      actionHTML = `<button class="primary-btn" style="padding: 0.4rem 0.8rem; font-size: 0.9rem;" onclick="openPaymentModal(${exp.id}, ${exp.amount})">Pay Now</button>`;
    } else {
      actionHTML = `<button class="valid-split-btn" style="padding: 0.4rem 0.8rem; font-size: 0.9rem; margin: 0;" onclick="updateStatus(${exp.id}, 'Pending', null)">Revert to Pending</button>`;
    }

    tr.innerHTML = `
      <td>${exp.date}</td>
      <td>${getRoomTagHTML(exp.room)}</td>
      <td>${exp.type}</td>
      <td>RM${exp.amount.toFixed(2)}</td>
      <td>${statusHTML}</td>
      <td>${actionHTML}</td>
    `;
    tbody.appendChild(tr);
  });
}

window.updateStatus = async function(id, newStatus, paymentMethod) {
  try {
    const payload = { status: newStatus };
    if (paymentMethod) {
      payload.payment_method = paymentMethod;
    }

    const res = await fetch(`${API_BASE}/expenses/${id}/status`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });
    
    if (res.ok) {
      fetchPayments(); // Refresh list
    } else {
      const errData = await res.json();
      alert('Error updating status: ' + (errData.error || 'Unknown error'));
    }
  } catch(err) {
    console.error(err);
    alert('Error connecting to backend');
  }
};

// Modal Logic
window.openPaymentModal = function(id, amount) {
  currentPayingId = id;
  modalAmountEl.textContent = `RM${amount.toFixed(2)}`;
  paymentModal.style.display = 'flex';
  
  // reset UI
  modalPaymentMethodSelect.value = 'Bank Transfer';
  updateDummyUI('Bank Transfer');
};

if (closePaymentModalBtn) {
  closePaymentModalBtn.onclick = () => {
    paymentModal.style.display = 'none';
    currentPayingId = null;
  };
}

window.onclick = (event) => {
  if (event.target === paymentModal) {
    paymentModal.style.display = 'none';
    currentPayingId = null;
  }
};

// Handle Payment Method dropdown change
if (modalPaymentMethodSelect) {
  modalPaymentMethodSelect.addEventListener('change', (e) => {
    updateDummyUI(e.target.value);
  });
}

function updateDummyUI(method) {
  document.getElementById('dummy-bank-transfer').style.display = 'none';
  document.getElementById('dummy-ewallet').style.display = 'none';
  document.getElementById('dummy-card').style.display = 'none';
  document.getElementById('dummy-cash').style.display = 'none';

  if (method === 'Bank Transfer') {
    document.getElementById('dummy-bank-transfer').style.display = 'block';
  } else if (method === 'eWallet') {
    document.getElementById('dummy-ewallet').style.display = 'block';
  } else if (method === 'Card') {
    document.getElementById('dummy-card').style.display = 'block';
  } else if (method === 'Cash') {
    document.getElementById('dummy-cash').style.display = 'block';
  }
}

// Handle Confirm Payment
if (confirmPaymentBtn) {
  confirmPaymentBtn.onclick = async () => {
    if (!currentPayingId) return;
    
    const method = modalPaymentMethodSelect.value;
    // visual feedback
    const originalText = confirmPaymentBtn.textContent;
    confirmPaymentBtn.textContent = 'Processing...';
    confirmPaymentBtn.disabled = true;

    // Simulate small network delay for realism
    setTimeout(async () => {
      await updateStatus(currentPayingId, 'Paid', method);
      
      // cleanup
      confirmPaymentBtn.textContent = originalText;
      confirmPaymentBtn.disabled = false;
      paymentModal.style.display = 'none';
      currentPayingId = null;
    }, 800);
  };
}
