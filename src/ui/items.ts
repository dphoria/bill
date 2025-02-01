function getReceiptTable(): HTMLTableElement {
    return document.getElementById("receipt-table") as HTMLTableElement;
}

function updateSubtotal(): void {
    const table = getReceiptTable();
    let subtotal = 0;

    const itemPrices = table.querySelectorAll('td[id^="item-price-"]');
    itemPrices.forEach((item) => {
        const value = parseFloat(item.textContent || "0");
        subtotal += value;
    });

    const subtotalCell = table.querySelector('td#subtotal') as HTMLTableCellElement;
    subtotalCell.textContent = subtotal.toFixed(2);
}

function getExtraScaler(extra: string): number {
    const table = getReceiptTable();
    const extraPercentCell = table.querySelector(`td#${extra}-percent`) as HTMLTableCellElement;
    const extraPercent = parseFloat(extraPercentCell.textContent || "0");
    return extraPercent * 0.01;
}

function updateExtra(extra: string): void {
    const table = getReceiptTable();
    const subtotalCell = table.querySelector('td#subtotal') as HTMLTableCellElement;
    const extraAmount = parseFloat(subtotalCell.textContent || "0") * getExtraScaler(extra);
    const extraCell = table.querySelector(`td#${extra}`) as HTMLTableCellElement;
    extraCell.textContent = extraAmount.toFixed(2);
}

function getNumPersosnForItem(item: number): number {
    const table = getReceiptTable();
    const row = table.rows[item + 1];
    const checkboxes = row.querySelectorAll('input[type="checkbox"]');
    const checkedCheckboxes = Array.from(checkboxes).filter(checkbox => (checkbox as HTMLInputElement).checked);
    return checkedCheckboxes.length;
}

function updatePersonTotal(person: number): void {
    const table = getReceiptTable();
    let subtotal = 0;

    const itemPrices = table.querySelectorAll('td[id^="item-price-"]');
    itemPrices.forEach((itemPriceCell, itemIndex) => {
        const checkbox = table.querySelector(`input#person-${person}-check-${itemIndex}`) as HTMLInputElement;
        if (checkbox.checked) {
            const itemPrice = parseFloat(itemPriceCell.textContent || "0");
            subtotal += itemPrice / getNumPersosnForItem(itemIndex);
        }
    });

    const subtotalCell = table.querySelector(`td#person-${person}-subtotal`) as HTMLTableCellElement;
    subtotalCell.textContent = subtotal.toFixed(2);
    let total = subtotal;

    const extraTypes: string[] = ["tax", "tip"];
    extraTypes.forEach((extraType) => {
        const extraAmount = subtotal * getExtraScaler(extraType);
        total += extraAmount;
        const extraCell = table.querySelector(`td#person-${person}-${extraType}`) as HTMLTableCellElement;
        extraCell.textContent = extraAmount.toFixed(2);
    });

    const totalCell = table.querySelector(`td#person-${person}-total`) as HTMLTableCellElement;
    totalCell.textContent = total.toFixed(2);
}

function updateTotal(): void {
    updateSubtotal();
    updateExtra("tax");
    updateExtra("tip");

    const table = getReceiptTable();
    const subtotalCell = table.querySelector('td#subtotal') as HTMLTableCellElement;
    const taxCell = table.querySelector(`td#tax`) as HTMLTableCellElement;
    const tipCell = table.querySelector(`td#tip`) as HTMLTableCellElement;
    const total = parseFloat(subtotalCell.textContent || "0") + parseFloat(taxCell.textContent || "0") + parseFloat(tipCell.textContent || "0");

    const totalCell = table.querySelector('td#total') as HTMLTableCellElement;
    totalCell.textContent = total.toFixed(2);

    const numPersons = getNumPersons();
    for (let person = 0; person < numPersons; person++) {
        updatePersonTotal(person);
    }
}

function getNumItems(): number {
    const table = getReceiptTable();
    const numItems = table.querySelectorAll('button[id^="item-name-"]').length;
    return numItems;
}

function getNumPersons(): number {
    const table = getReceiptTable();
    const headerRow = table.rows[0];
    const numColumns = headerRow.querySelectorAll("td").length;
    const numPersons = numColumns - 3;
    return numPersons;
}

function addCheckBox(person: number, item: number) {
    const checkbox = document.createElement("input");
    checkbox.id = `person-${person}-check-${item}`;
    checkbox.type = "checkbox";
    checkbox.classList.add("inline-block");

    checkbox.addEventListener('change', () => updatePersonTotal(person));

    const table = getReceiptTable();
    const checkCell = table.rows[item + 1].cells[person + 3];
    checkCell.classList.add("justify-center", "items-center", "text-center");
    checkCell.appendChild(checkbox);
}

function addItem(name: string): void {
    const table = getReceiptTable();
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

    const numPersons = getNumPersons();
    for (let person = 0; person < numPersons; person++) {
        newRow.insertCell(-1);
        addCheckBox(person, numItems);
    }

    updateTotal();
}

function addPerson(name: string): void {
    const table = getReceiptTable();
    const headerRow = table.rows[0];
    const numItems = getNumItems();
    const personIndex = getNumPersons();

    const nameCell = headerRow.insertCell(-1);
    nameCell.classList.add("text-center");
    nameCell.textContent = name;

    for (let index = 0; index < numItems; index++) {
        const checkCell = table.rows[index + 1].insertCell(-1);
        addCheckBox(personIndex, index);
    }

    const extraTypes: string[] = ["subtotal", "tax", "tip", "total"];
    extraTypes.forEach((extraType, index) => {
        const rowIndex = index + numItems + 1;
        const extraCell = table.rows[rowIndex].insertCell(-1);
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
        const nameInput = document.querySelector("input#person-name") as HTMLInputElement;
        nameInput.focus();
    });

    addPersonOkButton.addEventListener("click", () => {
        addToTable("person", addPerson);
    });

    addItemButton.addEventListener("click", () => {
        addItemModal.classList.remove("hidden");
        const nameInput = document.querySelector("input#item-name") as HTMLInputElement;
        nameInput.focus();
    });

    addItemOkButton.addEventListener("click", () => {
        addToTable("item", addItem);
    });
});
