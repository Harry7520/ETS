$(document).ready(function () {
    // Function to save dropdown state to localStorage
    function saveDropdownState() {
        $('.sub-menu').each(function () {
            var id = $(this).parent().index(); // Using parent index as ID
            var isOpen = $(this).is(':visible');
            localStorage.setItem('dropdown_state_' + id, isOpen);
        });
    }

    // Function to load dropdown state from localStorage
    function loadDropdownState() {
        $('.sub-menu').each(function () {
            var id = $(this).parent().index(); // Using parent index as ID
            var isOpen = localStorage.getItem('dropdown_state_' + id);
            if (isOpen === 'true') {
                $(this).show();
                $(this).prev('.sub-btn').find('.dropdown').addClass('rotate');
            }
        });
    }

    // Load dropdown state when the page loads
    loadDropdownState();

    // Toggle sub menus
    $('.sub-btn').click(function () {
        var clickedSubMenu = $(this).next('.sub-menu');
        $('.sub-menu').not(clickedSubMenu).slideUp(); // Close other dropdowns
        $('.dropdown').not($(this).find('.dropdown')).removeClass('rotate'); // Remove rotation from other dropdown arrows
        clickedSubMenu.slideToggle(function () {
            // Save dropdown state after the toggle animation completes
            saveDropdownState();
        });
        $(this).find('.dropdown').toggleClass('rotate');
    });
});