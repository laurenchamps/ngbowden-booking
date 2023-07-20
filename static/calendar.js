const calendar = document.getElementById('calendar');
const title = document.getElementById('month-year');
const previousMonth = document.getElementById('previous-month');
const nextMonth = document.getElementById('next-month');
const errorModal = new bootstrap.Modal('#errorModal');
const modalTitle = document.getElementById('errorModalLabel');
const successModal = new bootstrap.Modal('#successModal');

const months = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
];

const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

const today = new Date();
let currentMonth = today.getMonth();
let currentYear = today.getFullYear();


function drawBlankCalendar() {
    // Create header row with each day of week
    for (let i = 0; i < 7; i++) {
        const headerCell = document.createElement('div');
        headerCell.classList.add('header-cell');

        const dayName = document.createElement('p');
        dayName.classList.add('day-name');
        dayName.textContent = days[i];

        headerCell.appendChild(dayName);

        calendar.appendChild(headerCell);
    }

    // Divide calendar into 42 boxes
    for (let i = 0; i < 42; i++) {
        const day = document.createElement('div');
        day.classList.add('day');

        const dayNumber = document.createElement('p');
        dayNumber.classList.add('day-number');

        day.appendChild(dayNumber);

        calendar.appendChild(day);
    }
}

function updateCalendar(month, year) {
    // Display month and year on calendar
    const monthWithYear = `${months[month]} ${year}`;
    title.textContent = monthWithYear;
    const calendarMonth = String(month + 1).padStart(2, '0');
    let events = document.querySelectorAll('.event');

    // Set the first day of the month
    const theFirst = new Date();

    theFirst.setMonth(month);
    theFirst.setFullYear(year);
    theFirst.setDate(1);

    // Get the day of month that first day falls on
    const firstDayOfMonth = theFirst.getDay();
    // Get the number of days in the month
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    // Populate calendar with numbers for each day
    const dayElements = calendar.querySelectorAll('.day');

    let dayCounter = 1;

    for (let i = 1; i < dayElements.length; i++) {
        const day = dayElements[i];
        const dayNumber = day.querySelector('.day-number');

        // Reset to blank
        dayNumber.textContent = '';
        day.setAttribute("id", "");
        events.forEach((event) => {
            event.remove();
        })
        
        // Add each day of month to calendar
        if (i >= firstDayOfMonth && dayCounter <= daysInMonth) {
            let formattedCounter = String(dayCounter).padStart(2, '0');
            dayNumber.textContent = dayCounter;
            let fullYear = `${year}-${calendarMonth}-${formattedCounter}`;
            day.setAttribute("id", fullYear);
            dayCounter++;
        }
    } 
}

function getPreviousMonth() {
    if (currentMonth === 0) {
        currentYear--;
        currentMonth = 11;
    } else {
    currentMonth--;
    }

    updateCalendar(currentMonth, currentYear);
    getEvents();
}

function getNextMonth() {
    if (currentMonth == 11) {
        currentYear++;
        currentMonth = 0;
    } else {
    currentMonth++;
    }

    updateCalendar(currentMonth, currentYear);
    getEvents();
}

function getEvents() {
    fetch(`${window.origin}/book/make-booking`)
    .then(response => response.json())
    .then(data => {
        data.forEach((event) => addEventToDOM(event));
    });
};

function addEventToDOM(event) {
    // Create new elements and add event details
    const myEvent = document.createElement('div');
    myEvent.classList.add('event');
    myEvent.setAttribute('data-id', event.id);
    
    const myP1 = document.createElement('p');
    const myP2 = document.createElement('p');
    
    myP1.textContent = event.event_name;
    myP2.textContent = `${event.start_time} - ${event.end_time}`;
    
    myEvent.appendChild(myP1);
    myEvent.appendChild(myP2);
    
    // For each day element if it has an id matching the event date, add event to calendar
    const dayElements = document.querySelectorAll('.day');
    for (let i = 0; i < dayElements.length; i++) {
        if (event.date == dayElements[i].id) {
            dayElements[i].appendChild(myEvent);
        }
    }
}


// function removeEventFromDOM(id) {
//     const events = document.querySelectorAll('.event');

//     for (item in events) {
//         if (item.dataset.id === id) {
//             item.remove();
//             console.log("Item removed");
//         }
//     }
// }


function createEvent(e) {
    // Prevent default form behaviour
    e.preventDefault();

    const newEvent = {
        event_name: document.getElementById('event-name').value,
        date: document.getElementById('date').value,
        start_time: document.getElementById('start-time').value,
        end_time: document.getElementById('end-time').value,
    }

    // Post new event details to server
    fetch('http://127.0.0.1:5000/book/make-booking', {
        method: "POST",
        body: JSON.stringify(newEvent),
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then((response) => {
        if (response.ok) {
            return response.json();
        }
        return response.json().then(data => {throw new Error(data.message)})
    })
    .then((data) => {
        addEventToDOM(data);
        successModal.show();
    })
    .catch((error) => {
        modalTitle.textContent = `${error}`;
        errorModal.show();
    });
}

// function editEvent(e) {
//     // Prevent default form behaviour
//     e.preventDefault();

//     const updatedEvent = {
//         new_event_name: document.getElementById('event-name').value,
//         new_date: document.getElementById('date').value,
//         new_start_time: document.getElementById('start-time').value,
//         new_end_time: document.getElementById('end-time').value,
//     }

//     // Post new event details to server
//     fetch('http://127.0.0.1:5000/book/edit-booking', {
//         method: "POST",
//         body: JSON.stringify(updatedEvent),
//         headers: {
//             "Content-Type": "application/json"
//         }
//     })
//     .then((response) => {
//         if (response.ok) {
//             return response.json();
//         }
//         return response.json().then(data => {throw new Error(data.message)})
//     })
//     .then((data) => {
//         console.log(data);
//         addEventToDOM(data);
//         successModal.show();
//     })
//     .catch((error) => {
//         modalTitle.textContent = `${error}`;
//         errorModal.show();
//     });
// }


// Reload page when successful booking modal is closed
document.getElementById('successOK').addEventListener(
    "click",
    function () {
        location.reload();
    }
);


function loadCalendar() {
    drawBlankCalendar();
    // Default load to current month
    const today = new Date();
    updateCalendar(today.getMonth(), today.getFullYear());
    getEvents();
}

function init() {
    document.addEventListener('DOMContentLoaded', loadCalendar);
}

init();

// Event listeners
previousMonth.addEventListener("click", getPreviousMonth);
nextMonth.addEventListener("click", getNextMonth);
document.querySelector('#event-form').addEventListener('submit', createEvent);



