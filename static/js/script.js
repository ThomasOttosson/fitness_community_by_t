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