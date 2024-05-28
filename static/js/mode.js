document.addEventListener('DOMContentLoaded', function() {
    const darkModeButton = document.querySelector('.dark-mode');
    const body = document.body;

    // Function to toggle dark mode
    function toggleDarkMode() {
        body.classList.toggle('dark-mode-variables');
        // Toggle 'active' class on material-icons-sharp spans
        darkModeButton.querySelectorAll('.material-icons-outlined').forEach(function(span) {
            span.classList.toggle('active');
        });
        // Save state to localStorage
        localStorage.setItem('darkModeEnabled', body.classList.contains('dark-mode-variables'));
    }

    // Add event listener for button click
    darkModeButton.addEventListener('click', toggleDarkMode);

    // Check localStorage for dark mode state on page load
    const isDarkModeEnabled = localStorage.getItem('darkModeEnabled') === 'true';
    if (isDarkModeEnabled) {
        toggleDarkMode();
    }
});