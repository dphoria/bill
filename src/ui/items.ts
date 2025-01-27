function updateSubtotal(table: HTMLTableElement): void {
    let subtotal = 0;

    const itemPrices = table.querySelectorAll('td[id^="item-price-"]');
    itemPrices.forEach((item) => {
        const value = parseFloat(item.textContent || "0");
        subtotal += value;
    });

    const subtotalCell = table.querySelector('td#subtotal') as HTMLTableCellElement;
    subtotalCell.textContent = subtotal.toFixed(2);
}

function updateExtra(table: HTMLTableElement, extra: string): void {
    const extraPercentCell = table.querySelector(`td#${extra}-percent`) as HTMLTableCellElement;
    const extraPercent = parseFloat(extraPercentCell.textContent || "0");
    const subtotalCell = table.querySelector('td#subtotal') as HTMLTableCellElement;
    const extraAmount = parseFloat(subtotalCell.textContent || "0") * extraPercent * 0.01;
    const extraCell = table.querySelector(`td#${extra}`) as HTMLTableCellElement;
    extraCell.textContent = extraAmount.toFixed(2);
}

function updateTotal(table: HTMLTableElement): void {
    updateSubtotal(table);
    updateExtra(table, "tax");
    updateExtra(table, "tip");

    const subtotalCell = table.querySelector('td#subtotal') as HTMLTableCellElement;
    const taxCell = table.querySelector(`td#tax`) as HTMLTableCellElement;
    const tipCell = table.querySelector(`td#tip`) as HTMLTableCellElement;
    const total = parseFloat(subtotalCell.textContent || "0") + parseFloat(taxCell.textContent || "0") + parseFloat(tipCell.textContent || "0");

    const totalCell = table.querySelector('td#total') as HTMLTableCellElement;
    totalCell.textContent = total.toFixed(2);
}

function addItem(name: string): void {
    const table = document.getElementById("receipt-table") as HTMLTableElement;
    const tbody = table.querySelector('tbody') as HTMLTableSectionElement;

    const count = 1;
    const price = 0.00;

    const newRow = tbody.insertRow(-1);
    const nameCell = newRow.insertCell(0);
    const countCell = newRow.insertCell(1);
    const priceCell = newRow.insertCell(2);

    nameCell.innerHTML = `<input type="button" id="item-name-${table.rows.length - 2}" value="${name}">`;

    countCell.textContent = count.toString();
    countCell.classList.add("text-center");

    priceCell.id = `item-price-${table.rows.length - 2}`;
    priceCell.textContent = price.toFixed(2);
    priceCell.classList.add("text-right");

    updateTotal(table);
}

document.addEventListener("DOMContentLoaded", () => {
    updateTotal(document.getElementById("receipt-table") as HTMLTableElement);
});
