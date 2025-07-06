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