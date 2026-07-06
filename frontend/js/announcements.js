// announcements.js

document.addEventListener('DOMContentLoaded', () => {
    renderAnnouncements();
});

function submitAnnouncement() {
    const title = document.getElementById("announceTitle").value.trim();
    const message = document.getElementById("announceMessage").value.trim();
    const level = document.getElementById("announceLevel").value;

    if (!title || !message) {
        alert("Please provide both a title and a message.");
        return;
    }

    const newAnnouncement = {
        id: Date.now().toString(),
        title: title,
        message: message,
        level: level,
        date: new Date().toLocaleDateString()
    };

    let announcements = JSON.parse(localStorage.getItem('globalAnnouncements')) || [];
    announcements.push(newAnnouncement);
    localStorage.setItem('globalAnnouncements', JSON.stringify(announcements));

    // Clear form
    document.getElementById("announceTitle").value = "";
    document.getElementById("announceMessage").value = "";
    document.getElementById("announceLevel").value = "info";

    renderAnnouncements();
}

function deleteAnnouncement(id) {
    let announcements = JSON.parse(localStorage.getItem('globalAnnouncements')) || [];
    announcements = announcements.filter(a => a.id !== id);
    localStorage.setItem('globalAnnouncements', JSON.stringify(announcements));
    renderAnnouncements();
}

function renderAnnouncements() {
    const list = document.getElementById("announcementsList");
    let announcements = JSON.parse(localStorage.getItem('globalAnnouncements')) || [];

    if (announcements.length === 0) {
        list.innerHTML = `<p style="color: #64748b; font-style: italic;">No active announcements currently broadcasted.</p>`;
        return;
    }

    list.innerHTML = announcements.reverse().map(a => `
        <div class="announcement-card level-${a.level}">
            <div class="announcement-content">
                <h4>${a.title}</h4>
                <p>${a.message}</p>
                <small style="color: #64748b; font-size: 0.8rem;">Posted on: ${a.date}</small>
            </div>
            <button class="btn-delete" onclick="deleteAnnouncement('${a.id}')">Remove</button>
        </div>
    `).join('');
}
