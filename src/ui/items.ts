let currentEditIndex: number = -1;
let isAddMode: boolean = false;
let isSubmitting: boolean = false;

const itemsListView = document.getElementById(
  "items-list-view",
) as HTMLDivElement;
const editItemView = document.getElementById(
  "edit-item-view",
) as HTMLDivElement;
const editItemForm = document.getElementById(
  "edit-item-form",
) as HTMLFormElement;
const editItemIndex = document.getElementById(
  "edit-item-index",
) as HTMLInputElement;
const editItemName = document.getElementById(
  "edit-item-name",
) as HTMLInputElement;
const editItemPrice = document.getElementById(
  "edit-item-price",
) as HTMLInputElement;
const cancelButton = document.getElementById(
  "cancel-button",
) as HTMLButtonElement;
const splitButton = document.getElementById(
  "split-button",
) as HTMLButtonElement;
const saveButton = document.getElementById("save-button") as HTMLButtonElement;
const addItemButton = document.getElementById(
  "add-item-button",
) as HTMLButtonElement;
const personsButton = document.getElementById(
  "persons-button",
) as HTMLButtonElement;
const splitButtonNav = document.getElementById(
  "split-button-nav",
) as HTMLButtonElement;
const editTitle = document.getElementById("edit-title") as HTMLHeadingElement;
const editSubtitle = document.getElementById(
  "edit-subtitle",
) as HTMLParagraphElement;
const loadingOverlay = document.getElementById(
  "loading-overlay",
) as HTMLElement;

function showItemsList(): void {
  itemsListView.classList.remove("hidden");
  editItemView.classList.add("hidden");
  currentEditIndex = -1;
  isAddMode = false;
  isSubmitting = false;
}

function showEditItem(index: number, name: string, price: number): void {
  currentEditIndex = index;
  isAddMode = false;
  editItemIndex.value = index.toString();
  editItemName.value = name;
  editItemPrice.value = price.toFixed(2);

  editTitle.textContent = "Edit Item";
  editSubtitle.textContent = "Modify item details";
  splitButton.classList.remove("hidden");

  itemsListView.classList.add("hidden");
  editItemView.classList.remove("hidden");

  editItemName.focus();
}

function showAddItem(): void {
  currentEditIndex = -1;
  isAddMode = true;
  editItemIndex.value = "";
  editItemName.value = "";
  editItemPrice.value = "";

  editTitle.textContent = "Add Item";
  editSubtitle.textContent = "Create a new item";
  splitButton.classList.add("hidden");

  itemsListView.classList.add("hidden");
  editItemView.classList.remove("hidden");

  editItemName.focus();
}

function showLoadingOverlay(): void {
  loadingOverlay.classList.remove("hidden");
}

function hideLoadingOverlay(): void {
  loadingOverlay.classList.add("hidden");
}

function setupItemClickHandlers(): void {
  const itemElements = document.querySelectorAll("[data-item-index]");
  itemElements.forEach((itemElement) => {
    itemElement.addEventListener("click", () => {
      const index = parseInt(
        itemElement.getAttribute("data-item-index") || "0",
      );
      const name = itemElement.getAttribute("data-item-name") || "";
      const price = parseFloat(
        itemElement.getAttribute("data-item-price") || "0",
      );
      showEditItem(index, name, price);
    });
  });
}

function handleCancel(): void {
  showItemsList();
}

async function handleSplit(): Promise<void> {
  if (currentEditIndex === -1 || isAddMode) {
    return;
  }

  try {
    const response = await fetch("/split_item", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        item_index: currentEditIndex,
      }),
    });

    if (response.ok) {
      window.location.reload();
    } else {
      console.error("Failed to split item");
    }
  } catch (error) {
    console.error("Error splitting item:", error);
  }
}

async function handleSave(): Promise<void> {
  if (isSubmitting) {
    console.log("Already submitting, ignoring duplicate request");
    return;
  }

  const name = editItemName.value.trim();
  const price = parseFloat(editItemPrice.value);

  if (!name || isNaN(price) || price < 0) {
    alert("Please enter a valid name and price");
    return;
  }

  isSubmitting = true;
  saveButton.disabled = true;
  saveButton.textContent = isAddMode ? "Adding..." : "Saving...";

  try {
    const endpoint = isAddMode ? "/add_item" : "/update_item";
    const body = isAddMode
      ? { name: name, price: price }
      : { item_index: currentEditIndex, name: name, price: price };

    console.log(`Submitting to ${endpoint}:`, body);

    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    console.log(`Response status: ${response.status}`);

    if (response.ok) {
      console.log("Success, reloading page...");
      window.location.reload();
    } else {
      console.error(`Failed to ${isAddMode ? "add" : "update"} item`);
      alert(
        `Failed to ${isAddMode ? "add" : "update"} item. Please try again.`,
      );
    }
  } catch (error) {
    console.error(`Error ${isAddMode ? "adding" : "updating"} item:`, error);
    alert(`Error ${isAddMode ? "adding" : "updating"} item. Please try again.`);
  } finally {
    isSubmitting = false;
    saveButton.disabled = false;
    saveButton.textContent = "Save";
  }
}

async function navigateToPersons(): Promise<void> {
  window.location.href = "/persons";
}

async function navigateToSplit(): Promise<void> {
  showLoadingOverlay();
  
  try {
    const response = await fetch("/prepare_split", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      const result = await response.json();
      console.log(
        `Prepared split: ${result.person_count} persons, ${result.item_count} items`,
      );
      window.location.href = "/extras";
    } else {
      const error = await response.json();
      hideLoadingOverlay();
      alert(error.error || "Failed to prepare split");
    }
  } catch (error) {
    console.error("Error preparing for split:", error);
    hideLoadingOverlay();
    alert("Error preparing for split. Please try again.");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  hideLoadingOverlay();
  
  cancelButton.addEventListener("click", handleCancel);
  splitButton.addEventListener("click", handleSplit);
  saveButton.addEventListener("click", handleSave);
  addItemButton.addEventListener("click", showAddItem);
  personsButton.addEventListener("click", navigateToPersons);
  splitButtonNav.addEventListener("click", navigateToSplit);

  setupItemClickHandlers();

  editItemForm.addEventListener("submit", (e) => {
    e.preventDefault();
    handleSave();
  });

  editItemName.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      editItemPrice.focus();
    }
  });

  editItemPrice.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleSave();
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !editItemView.classList.contains("hidden")) {
      handleCancel();
    }
  });
});
