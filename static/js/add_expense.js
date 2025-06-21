document.addEventListener('DOMContentLoaded', () => {
    const expenseForm = document.getElementById('expenseForm');

    expenseForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const date = document.getElementById('date').value;
        const name = document.getElementById('name').value;
        const category = document.getElementById('category').value;
        const amount = parseFloat(document.getElementById('amount').value);

        const newExpense = { date, name, category, amount };

        // Get existing expenses or create empty array
        let expenses = JSON.parse(localStorage.getItem('expenses')) || [];

        // Add new expense
        expenses.push(newExpense);

        // Save back to localStorage
        localStorage.setItem('expenses', JSON.stringify(expenses));

        // Optional: clear form
        expenseForm.reset();

        alert("Expense added successfully!");
    });
});
