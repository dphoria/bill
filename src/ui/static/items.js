"use strict";
function getReceiptTable() {
    return document.getElementById("receipt-table");
}
function updateSubtotal() {
    const table = getReceiptTable();
    let subtotal = 0;
    const itemPrices = table.querySelectorAll('td[id^="item-price-"]');
    itemPrices.forEach((item) => {
        const value = parseFloat(item.textContent || "0");
        subtotal += value;
    });
    const subtotalCell = table.querySelector('td#subtotal');
    subtotalCell.textContent = subtotal.toFixed(2);
}
function getExtraScaler(extra) {
    const table = getReceiptTable();
    const extraPercentCell = table.querySelector(`td#${extra}-percent`);
    const extraPercent = parseFloat(extraPercentCell.textContent || "0");
    return extraPercent * 0.01;
}
function updateExtra(extra) {
    const table = getReceiptTable();
    const subtotalCell = table.querySelector('td#subtotal');
    const extraAmount = parseFloat(subtotalCell.textContent || "0") * getExtraScaler(extra);
    const extraCell = table.querySelector(`td#${extra}`);
    extraCell.textContent = extraAmount.toFixed(2);
}
function getNumPersosnForItem(item) {
    const table = getReceiptTable();
    const row = table.rows[item + 1];
    const checkboxes = row.querySelectorAll('input[type="checkbox"]');
    const checkedCheckboxes = Array.from(checkboxes).filter(checkbox => checkbox.checked);
    return checkedCheckboxes.length;
}
function updatePersonTotal(person) {
    const table = getReceiptTable();
    let subtotal = 0;
    const itemPrices = table.querySelectorAll('td[id^="item-price-"]');
    itemPrices.forEach((itemPriceCell, itemIndex) => {
        const checkbox = table.querySelector(`input#person-${person}-check-${itemIndex}`);
        if (checkbox.checked) {
            const itemPrice = parseFloat(itemPriceCell.textContent || "0");
            subtotal += itemPrice / getNumPersosnForItem(itemIndex);
        }
    });
    const subtotalCell = table.querySelector(`td#person-${person}-subtotal`);
    subtotalCell.textContent = subtotal.toFixed(2);
    let total = subtotal;
    const extraTypes = ["tax", "tip"];
    extraTypes.forEach((extraType) => {
        const extraAmount = subtotal * getExtraScaler(extraType);
        total += extraAmount;
        const extraCell = table.querySelector(`td#person-${person}-${extraType}`);
        extraCell.textContent = extraAmount.toFixed(2);
    });
    const totalCell = table.querySelector(`td#person-${person}-total`);
    totalCell.textContent = total.toFixed(2);
}
function updateTotal() {
    updateSubtotal();
    updateExtra("tax");
    updateExtra("tip");
    const table = getReceiptTable();
    const subtotalCell = table.querySelector('td#subtotal');
    const taxCell = table.querySelector(`td#tax`);
    const tipCell = table.querySelector(`td#tip`);
    const total = parseFloat(subtotalCell.textContent || "0") + parseFloat(taxCell.textContent || "0") + parseFloat(tipCell.textContent || "0");
    const totalCell = table.querySelector('td#total');
    totalCell.textContent = total.toFixed(2);
    const numPersons = getNumPersons();
    for (let person = 0; person < numPersons; person++) {
        updatePersonTotal(person);
    }
}
function getNumItems() {
    const table = getReceiptTable();
    const numItems = table.querySelectorAll('button[id^="item-name-"]').length;
    return numItems;
}
function getNumPersons() {
    const table = getReceiptTable();
    const headerRow = table.rows[0];
    const numColumns = headerRow.querySelectorAll("td").length;
    const numPersons = numColumns - 3;
    return numPersons;
}
function addCheckBox(person, item) {
    const checkbox = document.createElement("input");
    checkbox.id = `person-${person}-check-${item}`;
    checkbox.type = "checkbox";
    checkbox.classList.add("inline-block");
    checkbox.addEventListener('change', updateTotal);
    const table = getReceiptTable();
    const checkCell = table.rows[item + 1].cells[person + 3];
    checkCell.classList.add("justify-center", "items-center", "text-center");
    checkCell.appendChild(checkbox);
}
function setItemFromInput(index) {
    const nameInput = document.querySelector("input#item-name");
    const countInput = document.querySelector("input#item-count");
    const priceINput = document.querySelector("input#item-price");
    const table = getReceiptTable();
    const row = table.rows[index + 1];
    row.querySelector(`#item-name-${index}`).textContent = nameInput.value;
    row.querySelector(`#item-count-${index}`).textContent = countInput.value;
    row.querySelector(`#item-price-${index}`).textContent = parseFloat(priceINput.value).toFixed(2);
}
function setItemClickHandler(index) {
    const editItemButton = document.querySelector(`button#item-name-${index}`);
    editItemButton.addEventListener("click", () => {
        const itemIndex = document.querySelector("input#item-index");
        itemIndex.value = index.toString();
        const table = getReceiptTable();
        const row = table.rows[index + 1];
        const itemNameButton = row.querySelector(`#item-name-${index}`);
        const itemCountCell = row.querySelector(`#item-count-${index}`);
        const itemPriceCell = row.querySelector(`#item-price-${index}`);
        document.querySelector("input#item-name").value = itemNameButton.textContent || "";
        document.querySelector("input#item-count").value = itemCountCell.textContent || "1";
        document.querySelector("input#item-price").value = itemPriceCell.textContent || "0.00";
        showModalWindow("item");
    });
}
function addItem(name) {
    const table = getReceiptTable();
    const numItems = getNumItems();
    const newRowIndex = numItems + 1;
    const newRow = table.insertRow(newRowIndex);
    newRow.classList.add("py-1", "hover:bg-gray-100", "dark:hover:bg-gray-700", "border-y");
    const nameCell = newRow.insertCell(0);
    const countCell = newRow.insertCell(1);
    const priceCell = newRow.insertCell(2);
    nameCell.innerHTML = `<button id="item-name-${numItems}"></button>`;
    nameCell.classList.add("sticky-column");
    countCell.id = `item-count-${numItems}`;
    countCell.classList.add("text-center");
    priceCell.id = `item-price-${numItems}`;
    priceCell.classList.add("text-right");
    const numPersons = getNumPersons();
    for (let person = 0; person < numPersons; person++) {
        newRow.insertCell(-1);
        addCheckBox(person, numItems);
    }
    setItemFromInput(numItems);
    setItemClickHandler(numItems);
    updateTotal();
}
function addPerson(name) {
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
    const extraTypes = ["subtotal", "tax", "tip", "total"];
    extraTypes.forEach((extraType, index) => {
        const rowIndex = index + numItems + 1;
        const extraCell = table.rows[rowIndex].insertCell(-1);
        extraCell.classList.add("text-right", "px-1", "border-x");
        extraCell.id = `person-${personIndex}-${extraType}`;
        extraCell.textContent = "0.00";
    });
}
function showModalWindow(itemType) {
    const modalWindow = document.getElementById(`add-${itemType}-modal`);
    modalWindow.classList.remove("hidden");
    const nameInput = document.querySelector(`input#${itemType}-name`);
    nameInput.focus();
}
function hideModalWindow(itemType) {
    const modalWindow = document.getElementById(`add-${itemType}-modal`);
    modalWindow.classList.add("hidden");
    const nameInput = document.querySelector(`input#${itemType}-name`);
    nameInput.value = "";
}
function addToTable(itemType, doAdd) {
    const nameInput = document.getElementById(`${itemType}-name`);
    const name = nameInput.value.trim();
    if (name) {
        doAdd(name);
    }
    hideModalWindow(itemType);
}
document.addEventListener("DOMContentLoaded", () => {
    updateTotal();
    const addPersonButton = document.getElementById("add-person-button");
    const addPersonOkButton = document.getElementById("add-person-ok-button");
    const addItemButton = document.getElementById("add-item-button");
    const addItemOkButton = document.getElementById("add-item-ok-button");
    addPersonButton.addEventListener("click", () => {
        showModalWindow("person");
    });
    addPersonOkButton.addEventListener("click", () => {
        addToTable("person", addPerson);
    });
    addItemButton.addEventListener("click", () => {
        const itemIndex = document.querySelector("input#item-index");
        itemIndex.value = "-1";
        showModalWindow("item");
    });
    addItemOkButton.addEventListener("click", () => {
        const itemIndex = document.querySelector("input#item-index");
        const isNewItem = itemIndex.value === "-1";
        if (isNewItem) {
            addToTable("item", addItem);
        }
        else {
            setItemFromInput(parseInt(itemIndex.value));
            hideModalWindow("item");
            updateTotal();
        }
    });
    const numItems = getNumItems();
    for (let item = 0; item < numItems; item++) {
        setItemClickHandler(item);
    }
});
