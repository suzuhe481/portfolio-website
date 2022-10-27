/*
Toggles between adding and removing the "responsive" class 
to topnav when the user clicks on the hamburger menu icon.
*/
function toggleResponsive() {
    var x = document.getElementById("nav-bar");
    if (x.className === "topnav") {
        x.className += " responsive";
    } else {
        x.className = "topnav";
    }
}

/*
Displays the Projects dropdown menu when clicked.
*/
function toggleDropdown() {
    document.getElementById("dropdown-content").classList.toggle("show");
}

/*
Description: Closes the Projects dropdown menu if the user clicks outside of it.
*/
window.onclick = function(event) {
    if (!event.target.matches("#dropdown-button")) {
        var dropdown = document.getElementById("dropdown-content");

        if (dropdown.classList.contains("show")) {
            // dropdown.classList.remove("show");
            toggleDropdown();
        }
    }
}
