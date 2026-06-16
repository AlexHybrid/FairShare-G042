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