/**
 * CorruptiNO asosiy Javascript fayli
 */

// DOMContentLoaded - sahifa yuklangandan so'ng ishga tushadi
document.addEventListener('DOMContentLoaded', function() {

    // Xabar (alert)larini avtomatik yopish
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000); // 5 soniyadan so'ng

    // Tooltip va Popover (Bootstrap)larni aktivlashtirish
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));

    // Test topshirish sahifasida vaqt cheklovini qo'shish
    const testTimerElement = document.getElementById('test-timer');
    if (testTimerElement) {
        let timeLeft = parseInt(testTimerElement.dataset.timeLimit) || 300; // 5 daqiqa default

        const timerInterval = setInterval(function() {
            const minutes = Math.floor(timeLeft / 60);
            const seconds = timeLeft % 60;

            testTimerElement.textContent = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;

            if (--timeLeft < 0) {
                clearInterval(timerInterval);
                document.getElementById('test-form').submit(); // Vaqt tugaganda formani yuborish
            }
        }, 1000);
    }

    // Vakansiya filtrlash formasi
    const filterForm = document.getElementById('vacancy-filter-form');
    if (filterForm) {
        const filterInputs = filterForm.querySelectorAll('input, select');

        filterInputs.forEach(input => {
            input.addEventListener('change', function() {
                filterForm.submit();
            });
        });
    }

    // Vakansiya e'lon qilish formasida maosh validatsiyasi
    const salaryMinInput = document.getElementById('id_salary_min');
    const salaryMaxInput = document.getElementById('id_salary_max');

    if (salaryMinInput && salaryMaxInput) {
        const validateSalary = function() {
            const minValue = parseInt(salaryMinInput.value) || 0;
            const maxValue = parseInt(salaryMaxInput.value) || 0;

            if (minValue > maxValue && maxValue !== 0) {
                salaryMaxInput.setCustomValidity('Maksimal maosh minimal maoshdan katta bo\'lishi kerak');
            } else {
                salaryMaxInput.setCustomValidity('');
            }
        };

        salaryMinInput.addEventListener('input', validateSalary);
        salaryMaxInput.addEventListener('input', validateSalary);
    }

    // Test savol formasi uchun variant qo'shish
    const addOptionButton = document.getElementById('add-option-button');
    if (addOptionButton) {
        addOptionButton.addEventListener('click', function(e) {
            e.preventDefault();

            const optionsContainer = document.getElementById('options-container');
            const optionCount = optionsContainer.querySelectorAll('.option-row').length;

            if (optionCount < 4) { // Maksimal 4 ta variant
                const newOption = document.createElement('div');
                newOption.classList.add('option-row', 'mb-3');
                newOption.innerHTML = `
                    <div class="row">
                        <div class="col-md-8">
                            <input type="text" name="option_text_${optionCount + 1}" class="form-control" placeholder="Variant matni" required>
                        </div>
                        <div class="col-md-3">
                            <input type="number" name="option_points_${optionCount + 1}" class="form-control" placeholder="Ball" required>
                        </div>
                        <div class="col-md-1">
                            <button type="button" class="btn btn-danger btn-sm remove-option"><i class="fas fa-times"></i></button>
                        </div>
                    </div>
                `;

                optionsContainer.appendChild(newOption);

                // O'chirish tugmasini ishlashi
                const removeButton = newOption.querySelector('.remove-option');
                removeButton.addEventListener('click', function() {
                    optionsContainer.removeChild(newOption);
                });
            } else {
                alert('Maksimal 4 ta variant qo'shish mumkin!');
            }
        });
    }

    // Ishga qabul qilish jarayoni diagrammasi
    const hiringProcessChart = document.getElementById('hiring-process-chart');
    if (hiringProcessChart) {
        new Chart(hiringProcessChart, {
            type: 'bar',
            data: {
                labels: ['Arizalar', 'Test topshirish', 'Yakunlangan', 'Ko\'rib chiqilgan', 'Qabul qilingan'],
                datasets: [{
                    label: 'Nomzodlar soni',
                    data: [
                        hiringProcessChart.dataset.applications || 0,
                        hiringProcessChart.dataset.testing || 0,
                        hiringProcessChart.dataset.completed || 0,
                        hiringProcessChart.dataset.reviewed || 0,
                        hiringProcessChart.dataset.accepted || 0
                    ],
                    backgroundColor: [
                        'rgba(54, 162, 235, 0.6)',
                        'rgba(255, 206, 86, 0.6)',
                        'rgba(75, 192, 192, 0.6)',
                        'rgba(153, 102, 255, 0.6)',
                        'rgba(40, 167, 69, 0.6)'
                    ],
                    borderColor: [
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(40, 167, 69, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        precision: 0
                    }
                }
            }
        });
    }
});