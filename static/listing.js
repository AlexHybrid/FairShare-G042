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
        const agreementUrl = `/agreement?name=${encodeURIComponent(profile.name)}&room=${encodeURIComponent(activeRoom)}&index=${index}`;

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
