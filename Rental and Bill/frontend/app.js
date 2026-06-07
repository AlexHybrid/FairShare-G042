const API_BASE = 'http://localhost:5000/api';

let splitChartInstance = null;

// DOM Elements
const tbody = document.getElementById('dues-table-body');
const totalAmountEl = document.getElementById('total-amount');
const modal = document.getElementById('expense-modal');
const addBtn = document.getElementById('add-btn');
const closeBtn = document.getElementById('close-modal');
const form = document.getElementById('add-expense-form');

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
    tbody.innerHTML = `<tr><td colspan="4" style="text-align: center; color: #ff6b6b;">Error loading data. Is the backend running?</td></tr>`;
  }
}

// Render Table
function renderTable(expenses) {
  tbody.innerHTML = '';
  let total = 0;

  if (expenses.length === 0) {
    tbody.innerHTML = `<tr><td colspan="4" style="text-align: center;">No expenses found.</td></tr>`;
    totalAmountEl.textContent = 'TOTAL: RM0';
    return;
  }

  expenses.forEach(exp => {
    total += exp.amount;
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${exp.date}</td>
      <td>${exp.room}</td>
      <td>${exp.type}</td>
      <td>RM${exp.amount.toFixed(2)}</td>
    `;
    tbody.appendChild(tr);
  });

  totalAmountEl.textContent = `TOTAL: RM${total.toFixed(2)}`;
}

// Render Chart using Chart.js
function renderChart(expenses) {
  const ctx = document.getElementById('splitChart').getContext('2d');
  
  // Aggregate amounts by room
  const roomTotals = {};
  expenses.forEach(exp => {
    roomTotals[exp.room] = (roomTotals[exp.room] || 0) + exp.amount;
  });

  const labels = Object.keys(roomTotals);
  const data = Object.values(roomTotals);

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
        backgroundColor: [
          'rgba(0, 198, 255, 0.8)',
          'rgba(30, 60, 114, 0.8)',
          'rgba(44, 83, 100, 0.8)'
        ],
        borderColor: [
          '#00c6ff',
          '#1e3c72',
          '#2c5364'
        ],
        borderWidth: 1,
        hoverOffset: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
          labels: {
            color: '#e0e0e0',
            font: {
              family: "'Poppins', sans-serif"
            }
          }
        }
      }
    }
  });
}

// Modal interactions
addBtn.onclick = () => {
  modal.style.display = 'flex';
  // prefill date with today
  const today = new Date();
  const dd = String(today.getDate()).padStart(2, '0');
  const mm = String(today.getMonth() + 1).padStart(2, '0');
  const yy = String(today.getFullYear()).slice(-2);
  document.getElementById('date').value = `${dd}/${mm}/${yy}`;
};

closeBtn.onclick = () => {
  modal.style.display = 'none';
};

window.onclick = (event) => {
  if (event.target === modal) {
    modal.style.display = 'none';
  }
};

// Form Submission
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const newExpense = {
    date: document.getElementById('date').value,
    room: document.getElementById('room').value,
    type: document.getElementById('type').value,
    amount: parseFloat(document.getElementById('amount').value)
  };

  try {
    const res = await fetch(`${API_BASE}/expenses`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(newExpense)
    });

    if (res.ok) {
      modal.style.display = 'none';
      form.reset();
      fetchExpenses(); // Refresh the data
    } else {
      alert('Error adding expense');
    }
  } catch (err) {
    console.error(err);
    alert('Error connecting to backend');
  }
});
