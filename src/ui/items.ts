function updateSubtotal(): void {
    const table = document.getElementById("receipt-table") as HTMLTableElement;
    let subtotal = 0;

    const itemPrices = table.querySelectorAll('td[id^="item-price-"]');
    itemPrices.forEach((item) => {
        const value = parseFloat(item.textContent || "0");
        subtotal += value;
    });

    const subtotalCell = table.querySelector('td#subtotal') as HTMLTableCellElement;
    subtotalCell.textContent = subtotal.toFixed(2);
}

function updateExtra(extra: string): void {
    const table = document.getElementById("receipt-table") as HTMLTableElement;
    const extraPercentCell = table.querySelector(`td#${extra}-percent`) as HTMLTableCellElement;
    const extraPercent = parseFloat(extraPercentCell.textContent || "0");
    const subtotalCell = table.querySelector('td#subtotal') as HTMLTableCellElement;
    const extraAmount = parseFloat(subtotalCell.textContent || "0") * extraPercent * 0.01;
    const extraCell = table.querySelector(`td#${extra}`) as HTMLTableCellElement;
    extraCell.textContent = extraAmount.toFixed(2);
}

function updateTotal(): void {
    updateSubtotal();
    updateExtra("tax");
    updateExtra("tip");

    const table = document.getElementById("receipt-table") as HTMLTableElement;
    const subtotalCell = table.querySelector('td#subtotal') as HTMLTableCellElement;
    const taxCell = table.querySelector(`td#tax`) as HTMLTableCellElement;
    const tipCell = table.querySelector(`td#tip`) as HTMLTableCellElement;
    const total = parseFloat(subtotalCell.textContent || "0") + parseFloat(taxCell.textContent || "0") + parseFloat(tipCell.textContent || "0");

    const totalCell = table.querySelector('td#total') as HTMLTableCellElement;
    totalCell.textContent = total.toFixed(2);
}

function getNumItems(): number {
    const table = document.getElementById("receipt-table") as HTMLTableElement;
    const numItems = table.querySelectorAll('button[id^="item-name-"]').length;
    return numItems;
}

function addItem(name: string): void {
    const table = document.getElementById("receipt-table") as HTMLTableElement;
    const numItems = getNumItems();
    const newRowIndex = numItems + 1;

    const count = 1;
    const price = 0.00;

    const newRow = table.insertRow(newRowIndex);
    newRow.classList.add("py-1");

    const nameCell = newRow.insertCell(0);
    const countCell = newRow.insertCell(1);
    const priceCell = newRow.insertCell(2);

    nameCell.innerHTML = `<button id="item-name-${numItems}">${name}</button>`;

    countCell.textContent = count.toString();
    countCell.classList.add("text-center");

    priceCell.id = `item-price-${numItems}`;
    priceCell.textContent = price.toFixed(2);
    priceCell.classList.add("text-right");

    updateTotal();
}

function addPerson(name: string): void {
    const table = document.getElementById("receipt-table") as HTMLTableElement;
    const headerRow = table.rows[0];
    const numItems = getNumItems();
    const numColumns = headerRow.querySelectorAll("td").length;
    const personIndex = numColumns - 3;

    const nameCell = headerRow.insertCell(numColumns);
    nameCell.classList.add("text-center");
    nameCell.textContent = name;

    for (let index = 0; index < numItems; index++) {
        const checkbox = document.createElement("input");
        checkbox.id = `person-${personIndex}-check-${index}`;
        checkbox.type = "checkbox";
        checkbox.classList.add("inline-block");

        const checkCell = table.rows[index + 1].insertCell(-1);
        checkCell.classList.add("justify-center", "items-center", "text-center");
        checkCell.appendChild(checkbox);
    }

    const extraTypes: string[] = ["subtotal", "tax", "tip", "total"];
    extraTypes.forEach((extraType, index) => {
        const rowIndex = index + numItems + 1;
        const extraCell = table.rows[rowIndex].insertCell(numColumns);
        extraCell.classList.add("text-right");
        extraCell.id = `person-${personIndex}-${extraType}`;
        extraCell.textContent = "0.00";
    });
}

function addToTable(itemType: string, doAdd: (name: string) => void): void {
    const nameInput = document.getElementById(`${itemType}-name`) as HTMLInputElement;
    const name = nameInput.value.trim();

    if (name) {
        doAdd(name);
    }

    const addModal = document.getElementById(`add-${itemType}-modal`) as HTMLDivElement;
    addModal.classList.add("hidden");
    nameInput.value = "";
}

document.addEventListener("DOMContentLoaded", () => {
    updateTotal();

    const addPersonButton = document.getElementById("add-person-button") as HTMLButtonElement;
    const addPersonModal = document.getElementById("add-person-modal") as HTMLDivElement;
    const addPersonOkButton = document.getElementById("add-person-ok-button") as HTMLButtonElement;

    const addItemButton = document.getElementById("add-item-button") as HTMLButtonElement;
    const addItemModal = document.getElementById("add-item-modal") as HTMLDivElement;
    const addItemOkButton = document.getElementById("add-item-ok-button") as HTMLButtonElement;

    addPersonButton.addEventListener("click", () => {
        addPersonModal.classList.remove("hidden");
    });

    addPersonOkButton.addEventListener("click", () => {
        addToTable("person", addPerson);
    });

    addItemButton.addEventListener("click", () => {
        addItemModal.classList.remove("hidden");
    });

    addItemOkButton.addEventListener("click", () => {
        addToTable("item", addItem);
    });
});
