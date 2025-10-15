// This is the "brain" of our frontend. It handles all user interactions
// and communication with our backend API.

document.addEventListener('DOMContentLoaded', () => {

    //  Global Variables & Constants 
    const API_URL = 'http://127.0.0.1:5000';
    const $ = (selector) => document.querySelector(selector);

    //  Element Selectors 
    const loginSection = $('#login-section');
    const loginForm = $('#login-form');
    const registerFormContainer = $('#register-form-container');
    const registerForm = $('#register-form');
    const showRegisterLink = $('#show-register-link');
    const showLoginLink = $('#show-login-link');
    const authLinks = $('#auth-links');
    const userInfo = $('#user-info');
    const userEmailSpan = $('#user-email');
    const logoutBtn = $('#logout-btn');
    const addListingSection = $('#add-listing-section');
    const addListingForm = $('#add-listing-form');
    const listingsContainer = $('#listings-container');

    //  State Management 
    const state = {
        token: localStorage.getItem('authToken'),
    };



    /**
     * Fetches all available food listings from the backend and displays them.
     */
    async function fetchAndDisplayListings() {
        try {
            const response = await fetch(`${API_URL}/food/listings`);
            if (!response.ok) throw new Error('Failed to fetch listings.');
            const listings = await response.json();
            listingsContainer.innerHTML = ''; // Clear existing listings
            if (listings.length === 0) {
                listingsContainer.innerHTML = '<p>No available food listings at the moment.</p>';
                return;
            }
            listings.forEach(listing => {
                const item = document.createElement('div');
                item.className = 'listing-item';
                item.innerHTML = `
                    <h3>${listing.title}</h3>
                    <p><strong>Business:</strong> ${listing.business_name}</p>
                    <p>${listing.description}</p>
                    <p><strong>Quantity:</strong> ${listing.quantity}</p>
                    <p><strong>Price:</strong> $${parseFloat(listing.price).toFixed(2)}</p>
                    <button class="claim-btn" data-listing-id="${listing.id}">Claim 1</button>
                `;
                listingsContainer.appendChild(item);
            });
        } catch (error) {
            console.error('Error fetching listings:', error);
            listingsContainer.innerHTML = '<p>Could not load food listings. Please try again later.</p>';
        }
    }
    
    /**
     * Updates the UI based on whether a user is logged in or not.
     */
    function updateUIForAuthState() {
        if (state.token) {
            loginSection.classList.add('hidden');
            // We only show the "Add Listing" form if the user is a business.
            // For this basic version, we will just assume any logged in user can add.
            // A more advanced version would check the user's role.
            addListingSection.classList.remove('hidden'); 
            authLinks.classList.add('hidden');
            userInfo.classList.remove('hidden');
        } else {
            loginSection.classList.remove('hidden');
            addListingSection.classList.add('hidden');
            authLinks.classList.remove('hidden');
            userInfo.classList.add('hidden');
        }
    }

    //  Event Listeners 

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = $('#login-email').value;
        const password = $('#login-password').value;
        try {
            const response = await fetch(`${API_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password }),
            });
            if (!response.ok) throw new Error('Login failed. Please check your credentials.');
            const data = await response.json();
            state.token = data.access_token;
            localStorage.setItem('authToken', state.token);
            updateUIForAuthState();
            alert('Login successful!');
        } catch (error) {
            alert(error.message);
        }
    });
    
    addListingForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const title = $('#listing-title').value;
        const description = $('#listing-description').value;
        const quantity = $('#listing-quantity').value;
        const price = $('#listing-price').value;
        const expiry_time = new Date($('#listing-expiry').value).toISOString().slice(0, 19).replace('T', ' ');

        try {
            const response = await fetch(`${API_URL}/food/add`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${state.token}`
                },
                body: JSON.stringify({ title, description, quantity, price, expiry_time }),
            });

            if (!response.ok) throw new Error('Failed to add listing. You must be logged in.');

            alert('Listing added successfully!');
            addListingForm.reset();
            fetchAndDisplayListings(); 
        } catch (error) {
            alert(error.message);
        }
    });

    // --- NEW EVENT LISTENER ADDED BELOW ---

    /**
     * Handle clicks on the "Claim" buttons.
     * We use event delegation on the container for efficiency.
     */
    listingsContainer.addEventListener('click', async (e) => {
        // We only care about clicks on elements with the 'claim-btn' class
        if (e.target.classList.contains('claim-btn')) {
            if (!state.token) {
                alert('You must be logged in to claim an item.');
                return;
            }

            const listingId = e.target.dataset.listingId;
            
            try {
                const response = await fetch(`${API_URL}/claim`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${state.token}`
                    },
                    body: JSON.stringify({
                        listing_id: listingId,
                        quantity_claimed: 1 // For this basic UI, we'll always claim 1
                    })
                });

                if (!response.ok) throw new Error('Failed to claim item.');
                
                alert('Item claimed successfully!');
                fetchAndDisplayListings(); // Refresh the list to show the new quantity

            } catch (error) {
                alert(error.message);
            }
        }
    });

    logoutBtn.addEventListener('click', () => {
        state.token = null;
        localStorage.removeItem('authToken');
        updateUIForAuthState();
        alert('You have been logged out.');
    });

    showRegisterLink.addEventListener('click', (e) => {
        e.preventDefault();
        $('#login-form-container').classList.add('hidden');
        registerFormContainer.classList.remove('hidden');
    });
    
    showLoginLink.addEventListener('click', (e) => {
        e.preventDefault();
        $('#login-form-container').classList.remove('hidden');
        registerFormContainer.classList.add('hidden');
    });

    // --- Initial Setup ---
    fetchAndDisplayListings();
    updateUIForAuthState();
});

