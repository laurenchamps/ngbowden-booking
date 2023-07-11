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
    dayElements = calendar.querySelectorAll('.day');

    let dayCounter = 1;

    for (let i = 1; i < dayElements.length; i++) {
        const day = dayElements[i];
        const dayNumber = day.querySelector('.day-number');

        // Reset to blank
        dayNumber.textContent = '';
        
        // Add each day of month to calendar
        if (i >= firstDayOfMonth && dayCounter <= daysInMonth) {
            dayNumber.textContent = dayCounter;
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

drawBlankCalendar();
updateCalendar(6, 2023);

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
