/* jshint esversion: 8 */
/* jshint -W097 */ // This suppresses the "use strict" warning if not using the function wrapper
/* globals document, setInterval, alert, location */
// The above line configures JSHint for ES6 and declares global variables to prevent warnings.

'use strict';

/**
 * Updates the displayed current time every second.
 * @function updateTime
 */
function updateTime() {
  const now = new Date();
  const currentTimeElement = document.getElementById('current-time');
  if (currentTimeElement) {
    currentTimeElement.textContent = now.toLocaleTimeString();
  }
}

// Initialize and continuously update time if the element exists
if (document.getElementById('current-time')) {
  updateTime();
  setInterval(updateTime, 1000);
}

/**
 * Attaches an event listener to the user search input to filter the user table.
 * @constant userSearchInput
 */
const userSearchInput = document.getElementById('userSearch');
if (userSearchInput) {
  userSearchInput.addEventListener('input', function (e) {
    const searchTerm = e.target.value.toLowerCase();
    const rows = document.querySelectorAll('#usersTable tbody tr');

    rows.forEach((row) => {
      const usernameElement = row.querySelector(
        'td:first-child div:last-child div'
      );
      const emailElement = row.querySelector('td:nth-child(2) div');

      const username = usernameElement ? usernameElement.textContent.toLowerCase() : '';
      const email = emailElement ? emailElement.textContent.toLowerCase() : '';

      if (username.includes(searchTerm) || email.includes(searchTerm)) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    });
  });
}

/**
 * Attaches event listeners to filter radio buttons to show/hide user rows
 * based on data-user-type attribute.
 */
document.querySelectorAll('input[name="filter"]').forEach((radio) => {
  radio.addEventListener('change', function () {
    const filter = this.getAttribute('data-filter');
    const rows = document.querySelectorAll('#usersTable tbody tr');

    rows.forEach((row) => {
      const userType = row.getAttribute('data-user-type') || '';

      if (filter === 'all' || userType.includes(filter)) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    });
  });
});

/**
 * Placeholder function for exporting user data.
 * @function exportUsers
 */
function exportUsers() {
  alert('Export functionality would be implemented here');
}

/**
 * Reloads the page to refresh data.
 * @function refreshData
 */
function refreshData() {
  location.reload();
}

/**
 * Executes code after the DOM is fully loaded.
 * Handles card animation and attaches event listeners to buttons.
 */
document.addEventListener('DOMContentLoaded', function () {
  const cards = document.querySelectorAll('.hover-lift');
  cards.forEach((card, index) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    setTimeout(() => {
      card.style.transition = 'all 0.5s ease';
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, index * 100);
  });

  // Attach event listeners for functions to clear JSHint "unused" warnings
  const exportBtn = document.getElementById('exportUsersBtn');
  if (exportBtn) {
    exportBtn.addEventListener('click', exportUsers);
  }

  const refreshBtn = document.getElementById('refreshDataBtn');
  if (refreshBtn) {
    refreshBtn.addEventListener('click', refreshData);
  }
});

/**
 * Updates the current time displayed in the dashboard header.
 * Uses native Date and toLocaleTimeString for formatted output.
 */
function updateCurrentTime() {
  const now = new Date();
  const options = {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  };
  const timeElement = document.getElementById("current-time");
  if (timeElement) {
    timeElement.textContent = now.toLocaleTimeString(undefined, options);
  }
}

// Update time every second and call once on load
setInterval(updateCurrentTime, 1000);
updateCurrentTime();

/**
 * Placeholder function for exporting user data.
 * In a real application, this would trigger a backend process.
 */
function exportUsers() {
  alert("Export Users functionality coming soon!");
}

/**
 * Placeholder function for refreshing data.
 * Currently reloads the page.
 */
function refreshData() {
  alert("Refreshing data... (In a real app, this would re-fetch data).");
  location.reload();
}

/**
 * Filters the users table based on search input and selected radio filter.
 * Hides rows that do not match the criteria.
 */
function filterUsersTable() {
  const userSearchInput = document.getElementById("userSearch");
  const selectedFilterInput = document.querySelector(
    'input[name="filter"]:checked'
  );
  const usersTable = document.getElementById("usersTable");

  // Exit if critical elements are not found (e.g., script included on wrong page)
  if (!userSearchInput || !selectedFilterInput || !usersTable) {
    return;
  }

  const searchValue = userSearchInput.value.toLowerCase();
  const selectedFilter = selectedFilterInput.dataset.filter;
  const rows = usersTable.querySelectorAll("tbody tr");

  rows.forEach((row) => {
    const usernameElement = row.querySelector("td:nth-child(1) .fw-semibold");
    const emailElement = row.querySelector("td:nth-child(2) .fw-medium");
    const userTypes = row.dataset.userType || ""; // Default to empty string if not set

    const username = usernameElement ? usernameElement.textContent.toLowerCase() : '';
    const email = emailElement ? emailElement.textContent.toLowerCase() : '';

    const matchesSearch = username.includes(searchValue) || email.includes(searchValue);
    let matchesFilter = false;

    if (selectedFilter === "all") {
      matchesFilter = true;
    } else if (selectedFilter === "subscribers") {
      matchesFilter = userTypes.includes("subscriber");
    } else if (selectedFilter === "staff") {
      matchesFilter = userTypes.includes("staff");
    }

    // Set display property based on filter results
    row.style.display = (matchesSearch && matchesFilter) ? "" : "none";
  });
}

// Event listeners setup after the DOM is fully loaded
document.addEventListener("DOMContentLoaded", () => {
  const userSearchInput = document.getElementById("userSearch");
  if (userSearchInput) {
    userSearchInput.addEventListener("keyup", filterUsersTable);
  }

  const filterRadios = document.querySelectorAll('input[name="filter"]');
  filterRadios.forEach((radio) => {
    radio.addEventListener("change", filterUsersTable);
  });

  const exportBtn = document.getElementById("exportUsersBtn");
  if (exportBtn) {
    exportBtn.addEventListener("click", exportUsers);
  }

  const refreshBtn = document.getElementById("refreshDataBtn");
  if (refreshBtn) {
    refreshBtn.addEventListener("click", refreshData);
  }

  // Initial filter application when the page loads
  filterUsersTable();
});

// Stripe Payment Integration
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the checkout page by looking for the payment element container
    const paymentElementContainer = document.getElementById('payment-element-container');
    const stripeCredentials = document.getElementById('stripe-credentials');
    
    if (paymentElementContainer && stripeCredentials) {
        // Get credentials from the data attributes
        const stripePublishableKey = stripeCredentials.dataset.publishableKey;
        const clientSecret = stripeCredentials.dataset.clientSecret;
        
        if (!stripePublishableKey || !clientSecret) {
            paymentElementContainer.innerHTML = 
                '<div class="alert alert-danger">Payment configuration is missing. Please try again or contact support.</div>';
            return;
        }
        
        // Initialize Stripe with the publishable key
        const stripe = Stripe(stripePublishableKey);
        
        // Create Elements instance with the client secret
        const elements = stripe.elements({
            clientSecret: clientSecret
        });
        
        // Create and mount the Payment Element
        const paymentElement = elements.create('payment');
        paymentElement.mount(paymentElementContainer);
        
        // Set up form submission
        const form = document.getElementById('payment-form');
        const submitButton = document.getElementById('submit-button');
        const paymentMessage = document.getElementById('payment-message');
        
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            submitButton.disabled = true;
            
            const { error } = await stripe.confirmPayment({
                elements,
                confirmParams: {
                    return_url: window.location.origin + '/payment-success/',
                },
            });
            
            if (error) {
                if (error.type === "card_error" || error.type === "validation_error") {
                    paymentMessage.textContent = error.message;
                } else {
                    paymentMessage.textContent = "An unexpected error occurred.";
                }
                paymentMessage.classList.remove('hidden');
                submitButton.disabled = false;
            }
        });
    }
});