const API_BASE = '/api';

let splitChartInstance = null;

// DOM Elements
const tbody = document.getElementById('dues-table-body');
const totalAmountEl = document.getElementById('total-amount');
const modal = document.getElementById('expense-modal');
const addBtn = document.getElementById('add-btn');
const addBtnDashboard = document.getElementById('add-btn-dashboard');
const closeBtn = document.getElementById('close-modal');
const form = document.getElementById('add-expense-form');

// Theme room configuration for UI tags and Chart slices
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

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  fetchExpenses();
});

// Fetch data from Python backend
async function fetchExpenses() {
  try {
    const res = await fetch(`${API_BASE}/expenses`);
    if (!res.ok) throw new Error('Failed to fetch data');
    const data = await res.json();
    renderTable(data);
    renderChart(data);
  } catch (err) {
    console.error(err);
    tbody.innerHTML = `<tr><td colspan="4" style="text-align: center; color: #ff6b6b; font-weight: 500;">Error loading data. Is the backend running?</td></tr>`;
  }
}

// Render Table
function renderTable(expenses) {
  tbody.innerHTML = '';
  let total = 0;

  if (expenses.length === 0) {
    tbody.innerHTML = `<tr><td colspan="4" style="text-align: center; color: #94a3b8;">No expenses found.</td></tr>`;
    totalAmountEl.textContent = 'TOTAL: RM0.00';
    return;
  }

  expenses.forEach(exp => {
    total += exp.amount;
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${exp.date}</td>
      <td>${getRoomTagHTML(exp.room)}</td>
      <td>${exp.type}</td>
      <td>RM${exp.amount.toFixed(2)}</td>
    `;
    tbody.appendChild(tr);
  });

  totalAmountEl.textContent = `TOTAL: RM${total.toFixed(2)}`;
}

// Render Chart using Chart.js
function renderChart(expenses) {
  const canvasEl = document.getElementById('splitChart');
  if (!canvasEl) return;
  
  const ctx = canvasEl.getContext('2d');
  
  // Aggregate amounts by room
  const roomTotals = {};
  expenses.forEach(exp => {
    roomTotals[exp.room] = (roomTotals[exp.room] || 0) + exp.amount;
  });

  const labels = Object.keys(roomTotals);
  const data = Object.values(roomTotals);

  // Map theme colors to chart slices dynamically
  const backgroundColors = labels.map(room => (roomTheme[room] ? roomTheme[room].color : '#94a3b8'));
  const borderColors = backgroundColors;

  // If a chart already exists, destroy it before rendering a new one
  if (splitChartInstance) {
    splitChartInstance.destroy();
  }

  splitChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: backgroundColors,
        borderColor: '#111833', // Match panel bg
        borderWidth: 2,
        hoverOffset: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
          labels: {
            color: '#94a3b8',
            font: {
              family: "'Poppins', sans-serif",
              size: 12
            }
          }
        }
      }
    }
  });
}

// Modal interactions
const openModal = (e) => {
  if (e) e.preventDefault();
  modal.style.display = 'flex';
  // prefill date with today
  const today = new Date();
  const dd = String(today.getDate()).padStart(2, '0');
  const mm = String(today.getMonth() + 1).padStart(2, '0');
  const yy = String(today.getFullYear()).slice(-2);
  document.getElementById('date').value = `${dd}/${mm}/${yy}`;
};

if (addBtn) {
  addBtn.onclick = openModal;
}

if (addBtnDashboard) {
  addBtnDashboard.onclick = openModal;
}

if (closeBtn) {
  closeBtn.onclick = () => {
    modal.style.display = 'none';
  };
}

window.onclick = (event) => {
  if (event.target === modal) {
    modal.style.display = 'none';
  }
};

// File input: show selected filename
const receiptInput = document.getElementById('receipt');
const fileNameDisplay = document.getElementById('file-name-display');
if (receiptInput && fileNameDisplay) {
  receiptInput.addEventListener('change', () => {
    if (receiptInput.files.length > 0) {
      fileNameDisplay.textContent = receiptInput.files[0].name;
    } else {
      fileNameDisplay.textContent = 'Click to upload or drag & drop';
    }
  });
}

// Form Submission
form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const saveBtn = document.getElementById('save-expense-btn');
  if (saveBtn) { saveBtn.disabled = true; saveBtn.textContent = 'Saving…'; }

  let receiptPath = '';

  // 1. Upload receipt if provided
  const receiptFile = document.getElementById('receipt')?.files[0];
  if (receiptFile) {
    try {
      const formData = new FormData();
      formData.append('receipt', receiptFile);
      const uploadRes = await fetch(`${API_BASE}/expenses/upload`, {
        method: 'POST',
        body: formData
      });
      if (uploadRes.ok) {
        const uploadData = await uploadRes.json();
        receiptPath = uploadData.receipt_path || '';
      }
    } catch (err) {
      console.warn('Receipt upload failed, continuing without it:', err);
    }
  }

  // 2. Submit expense data
  const newExpense = {
    date:           document.getElementById('date').value,
    room:           document.getElementById('room').value,
    type:           document.getElementById('type').value,
    amount:         parseFloat(document.getElementById('amount').value),
    payment_method: document.getElementById('payment_method').value,
    category:       document.getElementById('category').value,
    notes:          document.getElementById('notes').value,
    receipt_path:   receiptPath,
    is_recurring:   document.getElementById('is_recurring').checked,
    status:         document.getElementById('status').value,
  };

  try {
    const res = await fetch(`${API_BASE}/expenses`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newExpense)
    });

    if (res.ok) {
      modal.style.display = 'none';
      form.reset();
      if (fileNameDisplay) fileNameDisplay.textContent = 'Click to upload or drag & drop';
      fetchExpenses(); // Refresh the data
    } else {
      alert('Error adding expense');
    }
  } catch (err) {
    console.error(err);
    alert('Error connecting to backend');
  } finally {
    if (saveBtn) { saveBtn.disabled = false; saveBtn.textContent = 'Save Expense'; }
  }
});

