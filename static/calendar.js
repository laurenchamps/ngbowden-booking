const calendar = document.getElementById('calendar');
const title = document.getElementById('month-year');
const previousMonth = document.getElementById('previous-month');
const nextMonth = document.getElementById('next-month');


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

        const event = document.createElement('p');
        event.classList.add('event');

        day.appendChild(dayNumber);
        day.appendChild(event);

        calendar.appendChild(day);
    }
}


function updateCalendar(month, year) {
    // Display month and year on calendar
    const monthWithYear = `${months[month]} ${year}`;
    title.textContent = monthWithYear;
    const calendarMonth = String(month + 1).padStart(2, '0');

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
        
        // Add each day of month to calendar
        if (i >= firstDayOfMonth && dayCounter <= daysInMonth) {
            let formattedCounter = String(dayCounter).padStart(2, '0');
            dayNumber.textContent = dayCounter;
            let fullYear = `${year}-${calendarMonth}-${formattedCounter}`;
            day.setAttribute("id", fullYear);
            dayCounter++;
        }
    } 

    getEvents();
}

function getPreviousMonth() {
    if (currentMonth === 0) {
        currentYear--;
        currentMonth = 11;
    } else {
    currentMonth--;
    }

    updateCalendar(currentMonth, currentYear);
}

function getNextMonth() {
    if (currentMonth == 11) {
        currentYear++;
        currentMonth = 0;
    } else {
    currentMonth++;
    }

    updateCalendar(currentMonth, currentYear);
}

function getEvents() {
    
    fetch(`${window.origin}/book/make-booking`)
    .then(function (response) {
        return response.json();
    }).then(function (object) {
        const dayElements = document.querySelectorAll('.day');

        // For each day in calendar
        for (let i = 0; i < dayElements.length; i++) {
            
            // Check for an event on the corresponding date and add event details to calendar
            for (let j = 0; j < object.length; j++) {
                if (object[j].start_date == dayElements[i].id) {
                    console.log(`There's an event today: ${object[j].start_date}`);
                    myEvent = document.createElement('p');
                    myEvent.classList.add('event');

                    myEvent.innerHTML = `${object[j].event_name}</br>${object[j].firstname}(${object[j].apartment})</br>${object[j].start_time} - ${object[j].end_time}`;
                    dayElements[i].appendChild(myEvent);
                }
            }
        }
        return object;
    });
}


drawBlankCalendar();
updateCalendar(6, 2023);


function make_booking() {
    const eventName = document.getElementById('event-name');
    const date = document.getElementById('date');
    const startTime = document.getElementById('start-time');
    const endTime = document.getElementById('end-time');

    const booking = {
        eventName: eventName.value,
        date: date.value,
        startTime: startTime.value,
        endTime: endTime.value,
    };

    fetch(`${window.origin}/book/make-booking`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(booking),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    })
}

// Event listeners
previousMonth.addEventListener("click", getPreviousMonth);
nextMonth.addEventListener("click", getNextMonth);

// Example fetch API request
// fetch('~~ add URL ~~')
//     .then((response) => {
//         return response.json();
//     })
//     .then((data) => {
//         console.log(data);
//     });
