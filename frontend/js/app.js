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
  renderTenantAnnouncements();
});

let allExpensesData = [];

// Render Tenant Announcements
function renderTenantAnnouncements() {
  const container = document.getElementById("tenantAnnouncements");
  if (!container) return; // Only run on dashboard
  
  const announcements = JSON.parse(localStorage.getItem('globalAnnouncements')) || [];
  const dismissed = JSON.parse(localStorage.getItem('dismissedAnnouncements')) || [];
  
  // Filter out dismissed announcements
  const activeAnnouncements = announcements.filter(a => !dismissed.includes(a.id));
  
  if (activeAnnouncements.length === 0) {
    container.innerHTML = "";
    return;
  }
  
  container.innerHTML = activeAnnouncements.map(a => {
    let bgColor, borderColor;
    if (a.level === 'info') { bgColor = 'rgba(59, 130, 246, 0.1)'; borderColor = '#3b82f6'; }
    else if (a.level === 'warning') { bgColor = 'rgba(245, 158, 11, 0.1)'; borderColor = '#f59e0b'; }
    else { bgColor = 'rgba(239, 68, 68, 0.1)'; borderColor = '#ef4444'; }
    
    return `
      <div class="tenant-announcement" style="background: ${bgColor}; border-left: 4px solid ${borderColor}; padding: 1rem 1.5rem; margin-bottom: 1.5rem; border-radius: 8px; display: flex; justify-content: space-between; align-items: flex-start; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <div>
          <h4 style="margin: 0 0 0.25rem 0; color: #fff; font-size: 1.05rem; font-family: 'Poppins', sans-serif;">📢 ${a.title}</h4>
          <p style="margin: 0; color: #e2e8f0; font-size: 0.95rem;">${a.message}</p>
        </div>
        <button onclick="dismissAnnouncement('${a.id}')" style="background: transparent; border: none; color: #94a3b8; font-size: 1.5rem; cursor: pointer; padding: 0 0.5rem; line-height: 1;">&times;</button>
      </div>
    `;
  }).join('');
}

// Dismiss an announcement
window.dismissAnnouncement = function(id) {
  const dismissed = JSON.parse(localStorage.getItem('dismissedAnnouncements')) || [];
  dismissed.push(id);
  localStorage.setItem('dismissedAnnouncements', JSON.stringify(dismissed));
  renderTenantAnnouncements();
};


// Fetch data from Python backend
// This function talks to the backend (get_expenses) to retrieve the latest expense list
// and then automatically triggers rendering the table and donut chart with the fetched data.
async function fetchExpenses() {
  try {
    const res = await fetch(`${API_BASE}/expenses`);
    if (!res.ok) throw new Error('Failed to fetch data');
    const data = await res.json();
    allExpensesData = data;
    renderTable(data);
    renderChart(data);
  } catch (err) {
    console.error(err);
    tbody.innerHTML = `<tr><td colspan="4" style="text-align: center; color: #ff6b6b; font-weight: 500;">Error loading data. Is the backend running?</td></tr>`;
  }
}

// Render Table
// This function takes the expense data array and dynamically creates HTML <tr> rows for the Dues Table.
// It also calculates the total pending amount and updates the footer.
function renderTable(expenses) {
  tbody.innerHTML = '';
  let total = 0;

  if (expenses.length === 0) {
    tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: #94a3b8;">No expenses found.</td></tr>`;
    if (totalAmountEl) {
      totalAmountEl.textContent = 'PENDING TOTAL: RM0.00';
    }
    return;
  }

  expenses.forEach(exp => {
    if (exp.status.toLowerCase() !== 'paid') {
      total += exp.amount;
    }
    const tr = document.createElement('tr');
    
    let statusHTML = '';
    if (exp.status.toLowerCase() === 'paid') {
      statusHTML = `<span class="tag tag-green">Paid</span>`;
    } else {
      statusHTML = `<span class="tag tag-yellow">Pending</span>`;
    }
    
    tr.innerHTML = `
      <td>${exp.date}</td>
      <td>${getRoomTagHTML(exp.room)}</td>
      <td>${exp.type}</td>
      <td>RM${exp.amount.toFixed(2)}</td>
      <td>${statusHTML}</td>
    `;
    tbody.appendChild(tr);
  });

  if (totalAmountEl) {
    totalAmountEl.textContent = `PENDING TOTAL: RM${total.toFixed(2)}`;
  }
}

// Render Chart using Chart.js
// This function groups the expense amounts by room/housemate and draws the donut chart visually.
function renderChart(expenses) {
  const canvasEl = document.getElementById('splitChart');
  if (!canvasEl) return;
  
  const ctx = canvasEl.getContext('2d');
  
  const roomTotals = {};
  expenses.forEach(exp => {
    if (exp.status.toLowerCase() !== 'paid') {
      roomTotals[exp.room] = (roomTotals[exp.room] || 0) + exp.amount;
    }
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

// Split Modal Logic
const validSplitBtn = document.querySelector('.valid-split-btn');
const splitModal = document.getElementById('split-modal');
const closeSplitModal = document.getElementById('close-split-modal');
const confirmSplitBtn = document.getElementById('confirm-split-btn');
const splitResultsContainer = document.getElementById('split-results-container');

if (validSplitBtn) {
  validSplitBtn.onclick = () => {
    if (allExpensesData.length === 0) {
      alert("No expenses available to split!");
      return;
    }
    
    let total = 0;
    const roomTotals = {
      'Room A': 0, 'Room B': 0, 'Room C': 0, 'Room D': 0, 'Room E': 0
    };
    
    allExpensesData.forEach(exp => {
      if (exp.status.toLowerCase() !== 'paid') {
        total += exp.amount;
        if (roomTotals[exp.room] !== undefined) {
          roomTotals[exp.room] += exp.amount;
        } else {
          roomTotals[exp.room] = exp.amount;
        }
      }
    });
    
    const numRooms = Object.keys(roomTotals).length;
    const perRoomShare = total / numRooms;
    
    let html = `<div style="background: rgba(255,255,255,0.05); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; text-align: center; border: 1px solid rgba(255,255,255,0.1);">
      <h3 style="margin: 0; color: #fff; font-size: 1.8rem; font-weight: 700;">Total: RM${total.toFixed(2)}</h3>
      <p style="margin: 0.5rem 0 0 0; color: #60a5fa; font-weight: 500; font-size: 1.1rem;">Divided among ${numRooms} rooms (RM${perRoomShare.toFixed(2)} per room)</p>
    </div>`;
    
    Object.keys(roomTotals).forEach(room => {
      const paid = roomTotals[room];
      const balance = perRoomShare - paid;
      
      let balanceHtml = '';
      if (balance > 0.01) {
        balanceHtml = `<span style="color: #fca5a5; font-weight: 600; font-size: 1rem;">Owes RM${balance.toFixed(2)}</span>`;
      } else if (balance < -0.01) {
        balanceHtml = `<span style="color: #4ade80; font-weight: 600; font-size: 1rem;">Receives RM${Math.abs(balance).toFixed(2)}</span>`;
      } else {
        balanceHtml = `<span style="color: #94a3b8; font-weight: 600; font-size: 1rem;">Settled</span>`;
      }
      
      html += `
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1); padding: 1rem 0;">
          <div style="display: flex; align-items: center; gap: 1rem;">
            ${getRoomTagHTML(room)}
            <span style="color: #94a3b8; font-size: 0.9rem;">(Paid: RM${paid.toFixed(2)})</span>
          </div>
          <div>${balanceHtml}</div>
        </div>
      `;
    });
    
    splitResultsContainer.innerHTML = html;
    splitModal.style.display = 'flex';
  };
}

if (closeSplitModal) {
  closeSplitModal.onclick = () => splitModal.style.display = 'none';
}
if (confirmSplitBtn) {
  confirmSplitBtn.onclick = () => splitModal.style.display = 'none';
}

window.onclick = (event) => {
  if (event.target === modal) {
    modal.style.display = 'none';
  }
  if (event.target === splitModal) {
    splitModal.style.display = 'none';
  }
  if (typeof beginnerModal !== 'undefined' && event.target === beginnerModal) {
    beginnerModal.style.display = 'none';
  }
};

// Beginner Modal Logic
const beginnerModal = document.getElementById('beginner-modal');
const closeBeginnerModalBtn = document.getElementById('close-beginner-modal');
const okBeginnerModalBtn = document.getElementById('ok-beginner-modal');

if (beginnerModal) {
  const navEntries = performance.getEntriesByType("navigation");
  const isReload = navEntries.length > 0 && navEntries[0].type === "reload";
  const isOldReload = performance.navigation && performance.navigation.type === 1;
  
  if (isReload || isOldReload) {
    beginnerModal.style.display = 'flex';
  }
}

if (closeBeginnerModalBtn) {
  closeBeginnerModalBtn.onclick = () => { if(beginnerModal) beginnerModal.style.display = 'none'; };
}
if (okBeginnerModalBtn) {
  okBeginnerModalBtn.onclick = () => { if(beginnerModal) beginnerModal.style.display = 'none'; };
}

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
// This intercepts the "Save Expense" button. It uploads the receipt (if present),
// sends the form data to the backend (add_expense route), and re-fetches data to update the UI.
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

