// Add Expense Form Validation and Submission
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('expenseForm');
    const successMessage = document.getElementById('successMessage');

    if (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            successMessage.classList.add('d-none');

            if (!form.checkValidity()) {
                event.stopPropagation();
                form.classList.add('was-validated');
                return;
            }

            // Simulate success (this will later be replaced with a real backend call)
            successMessage.classList.remove('d-none');
            form.reset();
            form.classList.remove('was-validated');
        });
    }
});
