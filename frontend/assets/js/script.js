// Поиск вакансий по названию
let form = document.querySelector('form');
let input = document.querySelector('#vacancy');
let vacancies = document.querySelectorAll('.card');
let nothingFoundAlert = document.querySelector('#nothingfound');

form.addEventListener('submit', function (event) {
    event.preventDefault();

    let searchTerm = input.value.trim().toLowerCase();
    let found = false;

    vacancies.forEach(function (vacancy) {
        let title = vacancy.querySelector('.card-title').textContent.toLowerCase();

        if (title.includes(searchTerm)) {
            vacancy.parentElement.style.display = 'block';
            found = true;
        } else {
            vacancy.parentElement.style.display = 'none';
        }
    });

    if (!found) {
        nothingFoundAlert.style.display = 'block';
    } else {
        nothingFoundAlert.style.display = 'none';
    }
});


function applyFilters() {
    let vacancies = document.querySelectorAll('.vacancy-item');
    let experienceFilters = Array.from(document.querySelectorAll('input[type="checkbox"][id^="checkbox1"], input[type="checkbox"][id^="checkbox2"], input[type="checkbox"][id^="checkbox3"]'))
        .filter(checkbox => checkbox.checked)
        .map(checkbox => checkbox.value);
    let employmentFilters = Array.from(document.querySelectorAll('input[type="checkbox"][id^="checkbox4"], input[type="checkbox"][id^="checkbox5"]'))
        .filter(checkbox => checkbox.checked)
        .map(checkbox => checkbox.value);

    let nothingFound = document.getElementById('nothingfound');
    let visibleVacancies = 0;

    vacancies.forEach(vacancy => {
        let experience = vacancy.getAttribute('data-experience');
        let employment = vacancy.getAttribute('data-employment');

        let experienceMatch = experienceFilters.length === 0 || experienceFilters.includes(experience);
        let employmentMatch = employmentFilters.length === 0 || employmentFilters.includes(employment);

        if (experienceMatch && employmentMatch) {
            vacancy.style.display = 'block';
            visibleVacancies++;
        } else {
            vacancy.style.display = 'none';
        }
    });

    nothingFound.style.display = visibleVacancies === 0 ? 'block' : 'none';
    console.log('Visible Vacancies:', visibleVacancies);
}

document.addEventListener('DOMContentLoaded', applyFilters);