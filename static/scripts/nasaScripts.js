// Runs toggleCalendar on page refresh.
window.onload = toggleCalendar;


// Displays a calendar if the user picks "Get a Specified Image" from the dropdown.
function toggleCalendar() {
  var nasaForm = document.getElementById("nasa-form");
  var x = document.getElementsByClassName("customDate");
  console.log(nasaForm.value);

  if (nasaForm.value == "getCustom") {
    console.log("display calendar");
    var x = document.getElementsByClassName("customDate");
    for (var i = 0; i < x.length; i++) {
      x[i].style.display = "block";
    }
  }
  else {
    console.log("hide calendar");
    var x = document.getElementsByClassName("customDate");
    for (var i = 0; i < x.length; i++) {
      x[i].style.display = "none";
    }
  }
}


// Script sets a specific range of dates for the calendar date picker.
// This script allows the user to clear the page of data.
var today = new Date();
var currentDay = today.getDate();
var currentMonth = today.getMonth() + 1; //January is 0!
var currentYear = today.getFullYear();
if(currentDay < 10) {
  currentDay='0'+ currentDay
} 
if(currentMonth < 10) {
  currentMonth='0'+ currentMonth
} 
today = currentYear + '-' + currentMonth + '-' + currentDay;
document.getElementById("customDate").setAttribute("max", today);


// Clears the page of images and data.
function clearPage() {
  document.getElementById("nasa_APOD_title").textContent = "";
  document.getElementById("nasa_APOD_date").textContent = "";
  document.getElementById("nasa_APOD_image").src = "";
  document.getElementById("nasa_APOD_video").src = "";
  document.getElementById("nasa_APOD_video").style = "display: none;"
  document.getElementById("nasa_APOD_exp").innerHTML = "";
}
