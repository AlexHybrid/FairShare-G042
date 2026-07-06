// Slide Navigation Configuration
let currentSlide = 1;
const totalSlides = 8;

// Speaker Scripts Database
const speakerScripts = {
    1: `
        <p><strong>Slide 1: Title Slide</strong></p>
        <p>Good day, everyone. Today I am excited to present our web application, a rental property expense management and lease tracking system designed for landlords and tenants: <strong>FairShare / Rental Blossoms</strong>.</p>
        <p>Managing shared housing expenses, tracking lease agreements, and organizing utility payments is often chaotic. Our goal was to create a modern, secure, and highly automated system that acts as a digital landlord assistant while providing tenants with a clear, visual dashboard.</p>
        <p>Let's navigate through the system architecture.</p>
    `,
    2: `
        <p><strong>Slide 2: System Architecture</strong></p>
        <p>First, let's talk about the technical backbone. We built our backend using <strong>Python and Flask</strong>, with <strong>SQLite</strong> handling database storage.</p>
        <p>Instead of building a single, heavy server, we opted for a <strong>microservice-inspired architecture</strong>. Here is how it is split:</p>
        <ul>
            <li><strong>Core API (Port 5000):</strong> Manages authentication, database writes, and handles scanned receipt uploads.</li>
            <li><strong>Excel Service (Port 5001):</strong> Isolated report server generating spreadsheets via <em>openpyxl</em>.</li>
            <li><strong>PDF Service (Port 5002):</strong> Custom document server compiling vector PDF files using <em>ReportLab</em>.</li>
        </ul>
        <p>By isolating exports onto separate ports, heavy printing jobs can run without locking database connections on the primary port.</p>
    `,
    3: `
        <p><strong>Slide 3: Database & Auto-Migration</strong></p>
        <p>Let's look at data management. We run a local SQLite database file, <code>rental_blossoms.db</code>. It is fully serverless and lightweight.</p>
        <p>One of our key developer additions is the <strong>automatic schema migration script</strong> in <code>database.py</code>. When the server launches, it queries the database columns in-place. If columns like <em>receipt_path</em> or <em>payment_method</em> are missing (due to a software update), it alters the tables automatically.</p>
        <p>This avoids crashing the server and, most importantly, protects the landlord's active transaction records from deletion.</p>
    `,
    4: `
        <p><strong>Slide 4: Tenant Dashboard & Bill Splitter</strong></p>
        <p>Now, let's explore the frontend. For the tenant, everything begins on the Dashboard powered by <code>app.js</code>.</p>
        <p>In addition to live transaction tables, we built an interactive <strong>Bill Splitter Calculator</strong> directly into the client script.</p>
        <p>Roommates can input any bill amount and specify the number of tenants, and the JavaScript instantly splits the math. This calculator has zero latency since it runs purely on the client side.</p>
    `,
    5: `
        <p><strong>Slide 5: Payments & Digital Agreement</strong></p>
        <p>Next is transaction handling and compliance.</p>
        <p>Our mock payment cashier (<code>payment.js</code>) simulates online checkouts for credit cards, bank transfers, or e-Wallets, automatically updating database balances upon completion.</p>
        <p>For lease contracts, we built an interactive drawing board. Roommates can sign agreements directly on the screen using their mouse or touchscreen. The canvas coordinates are compiled, converted to images, and saved on the server for compliance audits.</p>
    `,
    6: `
        <p><strong>Slide 6: Landlord Portal & Security Checks</strong></p>
        <p>For landlords, administrative security is paramount. We implemented <code>auth.js</code> to act as a gatekeeper.</p>
        <p>If a tenant tries to enter the admin view, they are blocked and prompted for a landlord PIN. Try it on the simulator: entering <strong>admin123</strong> unlocks the system.</p>
        <p>Once verified, the landlord can use the broadcast module to post notices directly onto the dashboard of every tenant in the building.</p>
    `,
    7: `
        <p><strong>Slide 7: Auditing & JSON Export Utilities</strong></p>
        <p>From a development and backup standpoint, we created the script <code>dump_data.py</code>.</p>
        <p>This developer utility queries the database and translates raw SQLite row objects into a formatted JSON output file called <code>Readable_Database.json</code>.</p>
        <p>This pretty-printed file gives developers and auditors a readable backup ledger in plain text without needing any SQLite database browser software.</p>
    `,
    8: `
        <p><strong>Slide 8: Summary & Q&A</strong></p>
        <p>To summarize, FairShare is a secure, responsive rental ecosystem. By separating document compilation into independent microservices, ensuring smooth database migrations, and providing landlords with admin security PIN locks, we've built a robust tool for property sharing.</p>
        <p>Thank you for your time. I am now open to any questions you might have.</p>
    `
};

// Initialize presentation
document.addEventListener('DOMContentLoaded', () => {
    goToSlide(currentSlide);
    setupKeyboardListeners();
    setupSignatureCanvas();
    runSplitter();
    
    // Setup landlord pin listeners
    const pinInput = document.getElementById('landlordPin');
    if (pinInput) {
        pinInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') verifyPin();
        });
    }
});

// Navigation Functions
function nextSlide() {
    if (currentSlide < totalSlides) {
        goToSlide(currentSlide + 1);
    }
}

function prevSlide() {
    if (currentSlide > 1) {
        goToSlide(currentSlide - 1);
    }
}

function goToSlide(index) {
    // Hide current slide
    const activeSlide = document.querySelector('.slide.active-slide');
    if (activeSlide) {
        activeSlide.classList.remove('active-slide');
    }
    
    // Show target slide
    const targetSlide = document.getElementById(`slide-${index}`);
    if (targetSlide) {
        targetSlide.classList.add('active-slide');
    }
    
    currentSlide = index;
    
    // Update indicator
    document.getElementById('slideIndicator').textContent = `${currentSlide} / ${totalSlides}`;
    
    // Update speaker notes
    updateSpeakerNotes(currentSlide);
}

// Setup Keyboard Navigation
function setupKeyboardListeners() {
    document.addEventListener('keydown', (e) => {
        // Prevent action when user is typing in interactive form controls
        if (document.activeElement.tagName === 'INPUT' || document.activeElement.tagName === 'TEXTAREA') {
            return;
        }
        
        switch (e.key) {
            case 'ArrowRight':
            case 'Space':
            case ' ':
                e.preventDefault();
                nextSlide();
                break;
            case 'ArrowLeft':
                e.preventDefault();
                prevSlide();
                break;
            case 'n':
            case 'N':
                toggleNotesPanel();
                break;
            case 'f':
            case 'F':
                toggleFullScreen();
                break;
        }
    });
}

// Presenter Notes Toggles
function updateSpeakerNotes(slideIndex) {
    const notesContent = document.getElementById('notesContent');
    if (notesContent && speakerScripts[slideIndex]) {
        notesContent.innerHTML = speakerScripts[slideIndex];
    }
}

function toggleNotesPanel() {
    const notesPanel = document.getElementById('notesPanel');
    const btnToggleNotes = document.getElementById('btnToggleNotes');
    
    if (notesPanel) {
        notesPanel.classList.toggle('hidden');
        if (notesPanel.classList.contains('hidden')) {
            btnToggleNotes.style.background = 'rgba(255, 255, 255, 0.03)';
            btnToggleNotes.style.color = 'var(--text-secondary)';
        } else {
            btnToggleNotes.style.background = 'rgba(99, 102, 241, 0.15)';
            btnToggleNotes.style.color = '#A5B4FC';
        }
    }
}

// Fullscreen Handler
function toggleFullScreen() {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(err => {
            console.error(`Error attempting to enable fullscreen: ${err.message}`);
        });
    } else {
        document.exitFullscreen();
    }
}

// Slide 2: Architectural Details Highlights
const serviceDetails = {
    core: {
        title: "<i class='fa-solid fa-server'></i> Core Service Details (app.py: Port 5000)",
        desc: "This is the primary web gateway. It handles standard API routing, SQLite transaction queries (CRUD), security verification layers, and directories for uploaded receipts. By hosting this separately from exports, core user interactions remain responsive.",
        info: "Uses Flask-CORS to bypass web browser security blocks that would otherwise stop the frontend from sending data to the server."
    },
    excel: {
        title: "<i class='fa-regular fa-file-excel'></i> Excel Service Details (ExcelExport.py: Port 5001)",
        desc: "Dedicated spreadsheet generator using the 'openpyxl' library. It retrieves transaction details and writes them cell-by-cell into a workbook. Includes fallback validations, ensuring missing entries write default labels instead of crashing.",
        info: "Running on a separate port means long-running spreadsheet writes do not consume threads from the central API server."
    },
    pdf: {
        title: "<i class='fa-regular fa-file-pdf'></i> PDF Service Details (pdfExport.py: Port 5002)",
        desc: "A standalone document service that builds high-resolution vector PDF layouts. Uses the ReportLab library to construct templates, format currency columns into currency strings, and paint styled layout borders.",
        info: "PDF canvas generation is CPU-bound. Isolating it ensures that multiple download requests don't affect core transaction logins."
    }
};

function highlightArchDetail(service) {
    const detailsPanel = document.getElementById('archDetailsPanel');
    const cards = document.querySelectorAll('.service-node');
    
    // Toggle active state styling on diagrams
    cards.forEach(card => card.classList.remove('active-service'));
    document.querySelector(`.${service}-service`).classList.add('active-service');
    
    if (detailsPanel && serviceDetails[service]) {
        detailsPanel.innerHTML = `
            <h3>${serviceDetails[service].title}</h3>
            <p>${serviceDetails[service].desc}</p>
            <div class="highlight-info-box">
                <strong>Service Architecture:</strong> ${serviceDetails[service].info}
            </div>
            <button class="btn-clear" style="margin-top: 15px; font-size: 0.8rem;" onclick="resetArchOverview()">Back to Overview</button>
        `;
    }
}

function resetArchOverview() {
    const detailsPanel = document.getElementById('archDetailsPanel');
    const cards = document.querySelectorAll('.service-node');
    cards.forEach(card => card.classList.remove('active-service'));
    
    if (detailsPanel) {
        detailsPanel.innerHTML = `
            <h3><i class="fa-solid fa-circle-info"></i> Architectural Overview</h3>
            <p>Click or hover over any backend service to inspect its role and configuration in the microservices design.</p>
            <div class="highlight-info-box">
                <strong>Port Conflict Isolation:</strong> Two web services cannot run on the same port. Isolating reports prevents heavy layout operations from slowing down database writes.
            </div>
        `;
    }
}

// Slide 4: Interactive Bill Splitter Math
function runSplitter() {
    const amount = parseFloat(document.getElementById('calcAmount').value);
    const roommates = parseInt(document.getElementById('calcRoommates').value);
    const resultElement = document.getElementById('calcResult');
    
    if (isNaN(amount) || isNaN(roommates) || roommates <= 0 || amount < 0) {
        resultElement.textContent = "RM 0.00";
        return;
    }
    
    const splitVal = amount / roommates;
    resultElement.textContent = `RM ${splitVal.toFixed(2)}`;
}

// Slide 5: Interactive Canvas Drawing Board (Signature Pad)
let isDrawing = false;
let lastX = 0;
let lastY = 0;
let canvas, ctx;

function setupSignatureCanvas() {
    canvas = document.getElementById('signatureCanvas');
    if (!canvas) return;
    
    ctx = canvas.getContext('2d');
    ctx.strokeStyle = '#6366F1';
    ctx.lineJoin = 'round';
    ctx.lineCap = 'round';
    ctx.lineWidth = 3;
    
    // Mouse Event Listeners
    canvas.addEventListener('mousedown', (e) => {
        isDrawing = true;
        [lastX, lastY] = getCoordinates(e);
    });
    
    canvas.addEventListener('mousemove', (e) => {
        if (!isDrawing) return;
        draw(e);
    });
    
    canvas.addEventListener('mouseup', () => isDrawing = false);
    canvas.addEventListener('mouseout', () => isDrawing = false);
    
    // Touch Event Listeners for Mobile Presenters
    canvas.addEventListener('touchstart', (e) => {
        isDrawing = true;
        const touch = e.touches[0];
        const mouseEvent = new MouseEvent("mousedown", {
            clientX: touch.clientX,
            clientY: touch.clientY
        });
        canvas.dispatchEvent(mouseEvent);
    }, { passive: true });
    
    canvas.addEventListener('touchmove', (e) => {
        const touch = e.touches[0];
        const mouseEvent = new MouseEvent("mousemove", {
            clientX: touch.clientX,
            clientY: touch.clientY
        });
        canvas.dispatchEvent(mouseEvent);
    }, { passive: true });
    
    canvas.addEventListener('touchend', () => {
        const mouseEvent = new MouseEvent("mouseup", {});
        canvas.dispatchEvent(mouseEvent);
    });
}

function getCoordinates(e) {
    const rect = canvas.getBoundingClientRect();
    // Account for styling scaling
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    
    return [
        (e.clientX - rect.left) * scaleX,
        (e.clientY - rect.top) * scaleY
    ];
}

function draw(e) {
    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    const [currentX, currentY] = getCoordinates(e);
    ctx.lineTo(currentX, currentY);
    ctx.stroke();
    [lastX, lastY] = [currentX, currentY];
}

function clearSignatureCanvas() {
    if (ctx && canvas) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
}

// Slide 6: Landlord Authenticator PIN verification
function verifyPin() {
    const pin = document.getElementById('landlordPin').value;
    const errorMsg = document.getElementById('pinError');
    const pinBody = document.getElementById('pinEntryBody');
    const announceBody = document.getElementById('announcementBody');
    const cardHeader = document.querySelector('#landlordAuthCard .lock-status');
    
    if (pin === 'admin123') {
        errorMsg.style.display = 'none';
        pinBody.style.display = 'none';
        announceBody.style.display = 'block';
        
        cardHeader.innerHTML = '<i class="fa-solid fa-unlock"></i> Unlocked';
        cardHeader.classList.remove('lock-status');
        cardHeader.classList.add('widget-badge', 'unlocked');
    } else {
        errorMsg.style.display = 'block';
        document.getElementById('landlordPin').value = '';
    }
}

function postAnnouncement() {
    const textarea = document.getElementById('announceText');
    const text = textarea.value;
    
    if (!text.trim()) {
        alert("Please enter a notice message.");
        return;
    }
    
    alert(`Success: Notice Broadcasted!\n\n"${text}"`);
    textarea.value = '';
}
