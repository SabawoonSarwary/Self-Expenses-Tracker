document.addEventListener('DOMContentLoaded', () => {
    const tableBody = document.querySelector("#expenseTable tbody");
    const totalAmountSpan = document.getElementById("totalAmount");

    let total = 0;

    // Get expenses from localStorage
    const expenses = JSON.parse(localStorage.getItem('expenses')) || [];

    expenses.forEach(exp => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${exp.date}</td>
            <td>${exp.name}</td>
            <td>${exp.category}</td>
            <td>${exp.amount.toFixed(2)}</td>
        `;

        tableBody.appendChild(row);
        total += exp.amount;
    });

    totalAmountSpan.textContent = total.toFixed(2);
});
