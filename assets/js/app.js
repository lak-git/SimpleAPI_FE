const API_BASE_URL = "http://127.0.0.1:8000/api/v1";
const searchBtn = document.getElementById("search-btn");
const clearBtn = document.getElementById("clear-btn");
const searchInput = document.getElementById("filter-input");
const closeModalBtn = document.getElementById("close-modal-btn");
const modal = document.getElementById("pin-modal");

fetchAndDisplayPins();

searchBtn.addEventListener("click", () => {
    fetchAndDisplayPins(searchInput.value);
});
clearBtn.addEventListener("click", () => {
    searchInput.value = "";
    fetchAndDisplayPins();
});
searchInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
        fetchAndDisplayPins(searchInput.value);
    }
});
closeModalBtn.addEventListener("click", closeModal);
window.addEventListener("click", (event) => {
    if (event.target === modal) {
        closeModal();
    }
});

/**
 * Fetches the list of pins.
 */
async function fetchAndDisplayPins(filterQuery = "") {
    const container = document.getElementById("pins-container");
    container.innerHTML = "<p>Loading pins...</p>";

    try {
        let url = `${API_BASE_URL}/pins/?sort_by=created_at&order=desc`;
        
        if (filterQuery) {
            url += `&title=${encodeURIComponent(filterQuery)}`; 
        }
        
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        const pinsArray = data.pins;
        
        container.innerHTML = "";
        
        if (!pinsArray || pinsArray.length === 0) {
            container.innerHTML = "<p>No pins found.</p>";
            return;
        }

        pinsArray.forEach(pin => {
            const card = document.createElement("div");
            card.className = "pin-card";
            
            const formattedDate = new Date(pin.created_at).toLocaleDateString();
            
            card.innerHTML = `
                ${pin.image_link ? `<img src="${pin.image_link}" alt="Pin Image" style="max-width: 100%; border-radius: 4px; margin-bottom: 10px;">` : ''}
                <h3>${pin.title}</h3>
                <p style="font-size: 0.85em; color: var(--text-muted); margin-top: -10px; margin-bottom: 10px;">
                    By ${pin.author} on ${formattedDate}
                </p>
                <p>${pin.body.length > 60 ? pin.body.substring(0, 60) + '...' : pin.body}</p>
            `;
            
            card.addEventListener("click", () => {
                openModal(pin.pin_id);
            });
            
            container.appendChild(card);
        });
    } catch (error) {
        console.error("Error fetching pins:", error);
        container.innerHTML = `<p style="color:red;">Failed to load pins.</p>`;
    }
}


async function openModal(pinId) {
    const modal = document.getElementById("pin-modal");
    const titleElement = document.getElementById("modal-title");
    const bodyElement = document.getElementById("modal-body");
    
    modal.style.display = "block";
    titleElement.innerText = "Loading...";
    bodyElement.innerText = "";

    try {
        const response = await fetch(`${API_BASE_URL}/pins/${pinId}`);
        
        if (!response.ok) {
            throw new Error("Failed to fetch pin details");
        }

        const pinData = await response.json();
        const formattedDate = new Date(pinData.created_at).toLocaleDateString();
        
        titleElement.innerText = pinData.title;
        bodyElement.innerHTML = `
            <p style="color: var(--text-muted); font-size: 0.9em; margin-top: -15px;">
                <strong>Author:</strong> ${pinData.author} | <strong>Date:</strong> ${formattedDate}
            </p>
            ${pinData.image_link ? `<img src="${pinData.image_link}" style="max-width: 100%; border-radius: 8px; margin: 15px 0;">` : ''}
            <p style="line-height: 1.6;">${pinData.body}</p>
        `;
        
    } catch (error) {
        console.error("Error fetching single pin:", error);
        titleElement.innerText = "Error";
        bodyElement.innerText = "Could not load pin details. Please try again.";
    }
}


function closeModal() {
    document.getElementById("pin-modal").style.display = "none";
}