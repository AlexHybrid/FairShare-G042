// Default seed data (Rooms A to F)
const defaultRoomsData = {
    "Room A": [
        { name: "Alice Johnson", email: "alice.j@academy.com", role: "Student", status: "Signed" },
        { name: "Bob Smith", email: "bob.smith@academy.com", role: "Student", status: "Pending" }
    ],
    "Room B": [
        { name: "Charlie Brown", email: "charlie.b@academy.com", role: "Student", status: "Signed" }
    ],
    "Room C": [
        { name: "Diana Prince", email: "diana.p@academy.com", role: "Instructor", status: "Signed" },
        { name: "Evan Wright", email: "evan.w@academy.com", role: "Student", status: "Pending" }
    ],
    "Room D": [
        { name: "Fiona Gallagher", email: "fiona.g@academy.com", role: "Student", status: "Pending" }
    ],
    "Room E": [
        { name: "George Clark", email: "george.c@academy.com", role: "Student", status: "Signed" }
    ],
    "Room F": [
        { name: "Hannah Abbott", email: "hannah.a@academy.com", role: "Student", status: "Pending" }
    ]
};

// Initialize App State
let directoryData = {};
let activeRoom = "Room A";

// Load data from localStorage or seed it if empty
function initializeData() {
    const savedData = localStorage.getItem("roomDirectoryData");
    if (savedData) {
        directoryData = JSON.parse(savedData);
    } else {
        directoryData = defaultRoomsData;
        saveDataToStorage();
    }
    
    // Check if active room exists, otherwise default to first available
    const roomsList = Object.keys(directoryData);
    if (roomsList.length > 0 && !directoryData[activeRoom]) {
        activeRoom = roomsList[0];
    }
}

// Save directory data to localStorage
function saveDataToStorage() {
    localStorage.setItem("roomDirectoryData", JSON.stringify(directoryData));
}

// Helper: get initials from name
function getInitials(name) {
    if (!name) return "??";
    const parts = name.split(" ");
    if (parts.length >= 2) {
        return (parts[0][0] + parts[1][0]).toUpperCase();
    }
    return name.slice(0, 2).toUpperCase();
}

// Render Room Navigation Tabs
function renderRoomTabs() {
    const tabsContainer = document.getElementById("roomTabsContainer");
    tabsContainer.innerHTML = "";

    const rooms = Object.keys(directoryData);
    rooms.forEach(roomName => {
        const btn = document.createElement("button");
        btn.className = `tab-btn ${roomName === activeRoom ? 'active' : ''}`;
        btn.textContent = roomName;
        btn.onclick = () => selectRoom(roomName);
        tabsContainer.appendChild(btn);
    });

    // Add the "+ Add Room" tab button at the end
    const addRoomBtn = document.createElement("button");
    addRoomBtn.className = "tab-btn add-room-tab";
    addRoomBtn.innerHTML = "+ Add Room";
    addRoomBtn.onclick = () => openRoomModal();
    tabsContainer.appendChild(addRoomBtn);
}

// Switch active room
function selectRoom(roomName) {
    activeRoom = roomName;
    renderRoomTabs();
    renderProfiles();
}

// Render profile cards in the active room
function renderProfiles() {
    document.getElementById("activeRoomTitle").textContent = activeRoom;
    
    const profiles = directoryData[activeRoom] || [];
    document.getElementById("activeRoomCount").textContent = `${profiles.length} Member${profiles.length === 1 ? '' : 's'}`;

    const grid = document.getElementById("profilesGrid");
    grid.innerHTML = "";

    // Render existing user profiles
    profiles.forEach((profile, index) => {
        const initials = getInitials(profile.name);
        
        const card = document.createElement("div");
        card.className = "profile-card";
        
        // Set color of badge based on status
        const statusClass = profile.status.toLowerCase() === 'signed' ? 'signed' : 'pending';
        const statusText = profile.status.toLowerCase() === 'signed' ? '✓ Signed' : '⚠ Pending Signature';

        // URL query parameters to link directly to agreement page with prefilled information
        const agreementUrl = `agreement.html?name=${encodeURIComponent(profile.name)}&room=${encodeURIComponent(activeRoom)}&index=${index}`;

        card.innerHTML = `
            <div class="avatar">${initials}</div>
            <h4 class="profile-name">${profile.name}</h4>
            <span class="profile-role">${profile.role}</span>
            <span class="profile-email">${profile.email}</span>
            
            <span class="status-badge ${statusClass}">
                ${statusText}
            </span>

            <a href="${agreementUrl}" class="action-link">
                <button class="btn-action">
                    ${profile.status.toLowerCase() === 'signed' ? 'View Agreement' : 'Sign Agreement'}
                </button>
            </a>
        `;
        grid.appendChild(card);
    });

    // Append the "+ Add New Profile" card at the end of the grid
    const addCard = document.createElement("div");
    addCard.className = "profile-card add-profile-card";
    addCard.onclick = () => openMemberModal();
    addCard.innerHTML = `
        <div class="add-profile-icon">+</div>
        <div class="add-profile-text">Add New Profile</div>
    `;
    grid.appendChild(addCard);
}

// Modals Management
function openRoomModal() {
    document.getElementById("roomModal").classList.add("active");
    document.getElementById("newRoomName").focus();
}

function closeRoomModal() {
    document.getElementById("roomModal").classList.remove("active");
    document.getElementById("newRoomName").value = "";
}

function openMemberModal() {
    document.getElementById("modalTargetRoom").textContent = activeRoom;
    document.getElementById("memberModal").classList.add("active");
    document.getElementById("newMemberName").focus();
}

function closeMemberModal() {
    document.getElementById("memberModal").classList.remove("active");
    document.getElementById("newMemberName").value = "";
    document.getElementById("newMemberEmail").value = "";
    document.getElementById("newMemberRole").value = "";
    document.getElementById("newMemberStatus").value = "Pending";
}

// Handle Add Room Submission
function submitNewRoom() {
    const roomNameInput = document.getElementById("newRoomName");
    const roomName = roomNameInput.value.trim();

    if (!roomName) {
        alert("Please enter a room name.");
        return;
    }

    if (directoryData[roomName]) {
        alert("This room already exists!");
        return;
    }

    // Create new room key and initialize empty array
    directoryData[roomName] = [];
    saveDataToStorage();
    
    closeRoomModal();
    selectRoom(roomName); // auto-select the newly created room
}

// Handle Add Profile Submission
function submitNewMember() {
    const name = document.getElementById("newMemberName").value.trim();
    const email = document.getElementById("newMemberEmail").value.trim();
    const role = document.getElementById("newMemberRole").value.trim() || "Student";
    const status = document.getElementById("newMemberStatus").value;

    if (!name || !email) {
        alert("Name and Email are required fields.");
        return;
    }

    // Simple validation check
    if (!email.includes("@")) {
        alert("Please enter a valid email address.");
        return;
    }

    // Push to active room
    if (!directoryData[activeRoom]) {
        directoryData[activeRoom] = [];
    }

    directoryData[activeRoom].push({ name, email, role, status });
    saveDataToStorage();

    closeMemberModal();
    renderProfiles();
}

// Run on load
document.addEventListener('DOMContentLoaded', () => {
    initializeData();
    renderRoomTabs();
    renderProfiles();
});