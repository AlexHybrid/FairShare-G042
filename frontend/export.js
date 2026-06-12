const API_BASE = 'http://localhost:5000/api';

const tbody = document.getElementById('report-table-body');
const totalAmountEl = document.getElementById('report-total-amount');

// Room configurations for UI tags
const roomTheme = {
  'Room A': { tagClass: 'tag-green' },
  'Room B': { tagClass: 'tag-yellow' },
  'Room C': { tagClass: 'tag-red' },
  'Room D': { tagClass: 'tag-blue' },
  'Room E': { tagClass: 'tag-purple' }
};

// Helper to get room tag HTML
function getRoomTagHTML(room) {
  const config = roomTheme[room] || { tagClass: 'tag-blue' };
  return `<span class="tag ${config.tagClass}">${room}</span>`;
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  fetchReportExpenses();
});

// Fetch data from backend
async function fetchReportExpenses() {
  try {
    const res = await fetch(`${API_BASE}/expenses`);
    if (!res.ok) throw new Error('Failed to fetch data');
    const data = await res.json();
    renderReportTable(data);
  } catch (err) {
    console.error(err);
    tbody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: #ff6b6b; font-weight: 500;">Error loading report preview. Is the backend running?</td></tr>`;
  }
}

// Render Table
function renderReportTable(expenses) {
  tbody.innerHTML = '';
  let total = 0;

  if (expenses.length === 0) {
    tbody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: #64748b;">No expenses found to export.</td></tr>`;
    totalAmountEl.textContent = 'RM0.00';
    return;
  }

  expenses.forEach(exp => {
    total += exp.amount;
    const tr = document.createElement('tr');
    
    // Status tag styling
    const statusClass = exp.status.toLowerCase() === 'paid' ? 'tag-green' : 'tag-yellow';
    const statusTag = `<span class="tag ${statusClass}">${exp.status}</span>`;

    tr.innerHTML = `
      <td>${exp.date}</td>
      <td>${getRoomTagHTML(exp.room)}</td>
      <td>${exp.type}</td>
      <td>${exp.category}</td>
      <td>${exp.payment_method}</td>
      <td>${statusTag}</td>
      <td style="color: #64748b; font-style: italic;">${exp.notes || '-'}</td>
      <td style="font-weight: 600;">RM${exp.amount.toFixed(2)}</td>
    `;
    tbody.appendChild(tr);
  });

  totalAmountEl.textContent = `RM${total.toFixed(2)}`;
}
