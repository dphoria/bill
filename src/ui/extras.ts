// State management
let currentExtraEditIndex: number = -1;
let isExtraAddMode: boolean = false;
let isExtraSubmitting: boolean = false; // Prevent double submissions

// DOM elements
const extrasListView = document.getElementById(
  "extras-list-view",
) as HTMLDivElement;
const editExtraView = document.getElementById(
  "edit-extra-view",
) as HTMLDivElement;
const editExtraForm = document.getElementById(
  "edit-extra-form",
) as HTMLFormElement;
const editExtraIndex = document.getElementById(
  "edit-extra-index",
) as HTMLInputElement;
const editExtraName = document.getElementById(
  "edit-extra-name",
) as HTMLInputElement;
const editExtraPrice = document.getElementById(
  "edit-extra-price",
) as HTMLInputElement;
const extraCancelButton = document.getElementById(
  "cancel-button",
) as HTMLButtonElement;
const extraSaveButton = document.getElementById(
  "save-button",
) as HTMLButtonElement;
const addExtraButton = document.getElementById(
  "add-extra-button",
) as HTMLButtonElement;
const extraBackButton = document.getElementById(
  "back-button",
) as HTMLButtonElement;
const extraDoneButton = document.getElementById(
  "done-button",
) as HTMLButtonElement;
const extraEditTitle = document.getElementById(
  "edit-title",
) as HTMLHeadingElement;
const extraEditSubtitle = document.getElementById(
  "edit-subtitle",
) as HTMLParagraphElement;
const extraRatio = document.getElementById("extra-ratio") as HTMLSpanElement;

// Show the extras list view
function showExtrasList(): void {
  extrasListView.classList.remove("hidden");
  editExtraView.classList.add("hidden");
  currentExtraEditIndex = -1;
  isExtraAddMode = false;
  isExtraSubmitting = false; // Reset submission state
}

// Show the edit extra view for editing
function showEditExtra(index: number, name: string, price: number): void {
  currentExtraEditIndex = index;
  isExtraAddMode = false;
  editExtraIndex.value = index.toString();
  editExtraName.value = name;
  editExtraPrice.value = price.toFixed(2);

  // Removed title/subtitle update
  extrasListView.classList.add("hidden");
  editExtraView.classList.remove("hidden");
  editExtraName.focus();
  updateExtraRatio();
}

// Show the edit extra view for adding
function showAddExtra(): void {
  currentExtraEditIndex = -1;
  isExtraAddMode = true;
  editExtraIndex.value = "";
  editExtraName.value = "";
  editExtraPrice.value = "";

  // Removed title/subtitle update
  extrasListView.classList.add("hidden");
  editExtraView.classList.remove("hidden");
  editExtraName.focus();
  updateExtraRatio();
}

function updateExtraRatio(): void {
  const price = parseFloat(editExtraPrice.value);
  const itemsTotal = parseFloat(
    editExtraView.getAttribute("data-items-total") || "0",
  );
  if (!isNaN(price) && itemsTotal > 0) {
    const ratio = (price / itemsTotal) * 100;
    extraRatio.textContent = `${ratio.toFixed(2)}%`;
  } else {
    extraRatio.textContent = "";
  }
}

// Handle extra click to enter edit mode
function setupExtraClickHandlers(): void {
  const extraElements = document.querySelectorAll("[data-extra-index]");
  extraElements.forEach((element) => {
    element.addEventListener("click", () => {
      const index = parseInt(element.getAttribute("data-extra-index") || "0");
      const name = element.getAttribute("data-extra-name") || "";
      const price = parseFloat(element.getAttribute("data-extra-price") || "0");
      showEditExtra(index, name, price);
    });
  });
}

// Cancel button - return to list view
function handleExtraCancel(): void {
  showExtrasList();
}

// Save button - update the current extra or add new extra
async function handleExtraSave(): Promise<void> {
  // Prevent double submissions
  if (isExtraSubmitting) {
    console.log("Already submitting, ignoring duplicate request");
    return;
  }

  const name = editExtraName.value.trim();
  const price = parseFloat(editExtraPrice.value);

  if (!name || isNaN(price) || price < 0) {
    alert("Please enter a valid name and price");
    return;
  }

  // Set submitting state and disable save button
  isExtraSubmitting = true;
  extraSaveButton.disabled = true;
  extraSaveButton.textContent = isExtraAddMode ? "Adding..." : "Saving...";

  try {
    const endpoint = isExtraAddMode ? "/add_extra" : "/update_extra";
    const body = isExtraAddMode
      ? { name: name, price: price }
      : { extra_index: currentExtraEditIndex, name: name, price: price };

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
      // Reload the page to show updated extras
      window.location.reload();
    } else {
      console.error(`Failed to ${isExtraAddMode ? "add" : "update"} extra`);
      alert(
        `Failed to ${isExtraAddMode ? "add" : "update"} extra. Please try again.`,
      );
    }
  } catch (error) {
    console.error(
      `Error ${isExtraAddMode ? "adding" : "updating"} extra:`,
      error,
    );
    alert(
      `Error ${isExtraAddMode ? "adding" : "updating"} extra. Please try again.`,
    );
  } finally {
    // Reset submitting state
    isExtraSubmitting = false;
    extraSaveButton.disabled = false;
    extraSaveButton.textContent = "Save";
  }
}

// Navigation functions
async function navigateBack(): Promise<void> {
  window.location.href = "/distribute";
}

async function navigateDone(): Promise<void> {
  window.location.href = "/payments";
}

// Event listeners
document.addEventListener("DOMContentLoaded", () => {
  // Setup click handlers for extras
  setupExtraClickHandlers();

  // Navigation button handlers
  extraBackButton.addEventListener("click", navigateBack);
  extraDoneButton.addEventListener("click", navigateDone);
  addExtraButton.addEventListener("click", showAddExtra);

  // Form handlers
  extraCancelButton.addEventListener("click", handleExtraCancel);
  editExtraForm.addEventListener("submit", (e) => {
    e.preventDefault();
    handleExtraSave();
  });

  // Enter key handlers for form inputs
  editExtraName.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      editExtraPrice.focus();
    }
  });

  editExtraPrice.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      handleExtraSave();
    }
  });

  // Add event listener for price input
  editExtraPrice.addEventListener("input", updateExtraRatio);
});
