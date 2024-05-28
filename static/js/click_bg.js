document.addEventListener("DOMContentLoaded", function() {
    var items = document.querySelectorAll('.menu .item');
    var subItems = document.querySelectorAll('.menu .sub-item');

    var activeItemIndex = localStorage.getItem("activeItemIndex");
    var activeSubItemIndex = localStorage.getItem("activeSubItemIndex");

    if (activeItemIndex !== null) {
      setActiveItem(parseInt(activeItemIndex));
    }

    if (activeSubItemIndex !== null) {
      setActiveSubItem(parseInt(activeSubItemIndex));
      // Remove active class from items if there's an active sub-item
      clearActiveMainItems();
    }

    items.forEach(function(item, index) {
      item.addEventListener('click', function(event) {
        event.stopPropagation();
        setActiveItem(index);
        clearActiveSubItems();
        localStorage.setItem("activeItemIndex", index);
        localStorage.removeItem("activeSubItemIndex");
      });
    });

    subItems.forEach(function(subItem, index) {
      subItem.addEventListener('click', function(event) {
        event.stopPropagation();
        setActiveSubItem(index);
        setActiveMainItem(subItem.closest('.item')); // Set active main item
        localStorage.setItem("activeSubItemIndex", index);
      });
    });

    function setActiveItem(index) {
      items.forEach(function(item, i) {
        if (i === index) {
          item.classList.add('active');
        } else {
          item.classList.remove('active');
        }
      });
    }

    function setActiveSubItem(index) {
      subItems.forEach(function(subItem, i) {
        if (i === index) {
          subItem.classList.add('active');
        } else {
          subItem.classList.remove('active');
        }
      });
    }

    function setActiveMainItem(mainItem) {
      items.forEach(function(item) {
        if (item === mainItem) {
          item.classList.add('active');
        } else {
          item.classList.remove('active');
        }
      });
    }

    function clearActiveSubItems() {
      subItems.forEach(function(subItem) {
        subItem.classList.remove('active');
      });
    }

    function clearActiveMainItems() {
      items.forEach(function(item) {
        item.classList.remove('active');
      });
    }
  });