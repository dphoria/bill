let selectedPersons: number[] = [];
let currentItem: { name: string; price: number } | null = null;
let currentItemIndex: number = 0;
let totalItemCount: number = 0;

// Person-based distribution logic
let currentPersonIndex: number = 0;
let totalPersonCount: number = 0;
let persons: any[] = [];
let items: any[] = [];

const itemName = document.getElementById("item-name") as HTMLSpanElement;
const itemPrice = document.getElementById("item-price") as HTMLSpanElement;
const prevItemButton = document.getElementById(
  "prev-item-button",
) as HTMLButtonElement;
const nextItemButton = document.getElementById(
  "next-item-button",
) as HTMLButtonElement;
const backButton = document.getElementById("back-button") as HTMLButtonElement;
const distributeButton = document.getElementById(
  "distribute-button",
) as HTMLButtonElement;
const distributionResults = document.getElementById(
  "distribution-results",
) as HTMLDivElement;
const resultsList = document.getElementById("results-list") as HTMLDivElement;
const loadingOverlay = document.getElementById("loading-overlay") as HTMLElement;

const prevPersonButton = document.getElementById("prev-person-button") as HTMLButtonElement;
const nextPersonButton = document.getElementById("next-person-button") as HTMLButtonElement;
const personName = document.getElementById("person-name") as HTMLSpanElement;

const itemNameElement = document.getElementById(
  "item-name",
) as HTMLMetaElement;
const itemPriceElement = document.getElementById(
  "item-price",
) as HTMLMetaElement;

const personElements = document.querySelectorAll(".person-box");

document.addEventListener("DOMContentLoaded", async () => {
  prevItemButton.addEventListener("click", handlePrevItem);
  nextItemButton.addEventListener("click", handleNextItem);
  backButton.addEventListener("click", handleBack);
  distributeButton.addEventListener("click", handleDone);

  initializeItemData();
  initializePersonData();
  await fetchDistributeData();
  renderItemsForPerson();
  updateNavigationButtons();

  prevPersonButton.addEventListener("click", handlePrevPerson);
  nextPersonButton.addEventListener("click", handleNextPerson);

  // Attach click handlers to item boxes
  document.querySelectorAll(".item-box").forEach((itemBox) => {
    itemBox.addEventListener("click", handleItemBoxClick);
  });

  setupPersonSelectionHandlers();

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      handleBack();
    }
  });
});

function setupPersonSelectionHandlers(): void {
  const selectedPersonClasses = [
    "bg-green-600/30",
    "border-green-400",
    "border-2",
    "ring-4",
    "ring-green-400/40",
    "shadow-lg",
  ] as const;
  selectedPersons = [];

  personElements.forEach((personBox) => {
    const personId = parseInt(personBox.getAttribute("data-person-id") || "0");

    let addPerson = () => {
      console.log("Adding person", personId);
      selectedPersons.push(personId);
      personBox.classList.add(...selectedPersonClasses);
    };

    let removePerson = () => {
      console.log("Removing person", personId);
      personBox.classList.remove(...selectedPersonClasses);
    };

    const wasPersonSelected =
      personBox.getAttribute("data-selected") === "true";
    if (wasPersonSelected) {
      addPerson();
    }

    personBox.addEventListener("click", (e) => {
      const isPersonDeselected = selectedPersons.includes(personId);

      if (isPersonDeselected) {
        selectedPersons = selectedPersons.filter((id) => id !== personId);
        removePerson();
        personBox.setAttribute("data-selected", "false");
      } else {
        addPerson();
        personBox.setAttribute("data-selected", "true");
      }

      updateDistributeButton();
    });
  });

  updateDistributeButton();
}

function initializeItemData(): void {
  const itemCountElement = document.getElementById(
    "item-count",
  ) as HTMLMetaElement;
  const itemIndexElement = document.getElementById(
    "item-index",
  ) as HTMLMetaElement;
  const itemName = itemNameElement.content || "";
  const itemPrice = parseFloat(itemPriceElement.content || "0");

  currentItem = {
    name: itemName,
    price: itemPrice,
  };
  console.log("Current item", currentItem);

  updateNavigationButtons();
}

async function getCurrentItem(): Promise<void> {
  const itemIndex = getItemIndexFromUrl();

  if (itemIndex) {
    try {
      const response = await fetch(`/get_item?item_index=${itemIndex}`);
      if (response.ok) {
        const item = await response.json();
        currentItem = item;
        updateItemDisplay();
      }
    } catch (error) {
      console.error("Error fetching item:", error);
    }
  }
}

function updateItemDisplay(): void {
  if (currentItem) {
    itemName.textContent = currentItem.name;
    itemPrice.textContent = `$${currentItem.price.toFixed(2)}`;
  }
}

function getItemSharedCount(): number {
  return selectedPersons.length;
}

function updateDistributeButton(): void {
  const distributionClasses = ["opacity-50", "cursor-not-allowed"] as const;

  let isNoOneSelected = getItemSharedCount() === 0;
  distributeButton.disabled = isNoOneSelected;

  if (isNoOneSelected) {
    distributeButton.classList.add(...distributionClasses);
  } else {
    distributeButton.classList.remove(...distributionClasses);
  }

  updatePersonShares();
}

function updatePersonShares(): void {
  if (!currentItem) {
    return;
  }

  document.querySelectorAll(".person-share").forEach((element) => {
    (element as HTMLSpanElement).textContent = "$0.00";
  });

  const itemSharedCount = getItemSharedCount();
  if (itemSharedCount === 0) {
    return;
  }

  const sharePerPerson = currentItem.price / itemSharedCount;

  selectedPersons.forEach((personId) => {
    const shareElement = document.querySelector(
      `.person-share[data-person-id="${personId}"]`,
    ) as HTMLSpanElement;
    if (shareElement) {
      shareElement.textContent = `$${sharePerPerson.toFixed(2)}`;
    }
  });
}

async function handlePrevItem(): Promise<void> {
  if (currentItemIndex > 0) {
    await saveCurrentDistribution();
    window.location.href = `/distribute?item_index=${currentItemIndex - 1}`;
  }
}

async function handleNextItem(): Promise<void> {
  if (currentItemIndex < totalItemCount - 1) {
    await saveCurrentDistribution();
    window.location.href = `/distribute?item_index=${currentItemIndex + 1}`;
  }
}

function updateNavigationButtons(): void {
  const navigationClasses = ["opacity-50", "cursor-not-allowed"] as const;

  prevItemButton.disabled = currentItemIndex <= 0;
  if (currentItemIndex <= 0) {
    prevItemButton.classList.add(...navigationClasses);
  } else {
    prevItemButton.classList.remove(...navigationClasses);
  }

  nextItemButton.disabled = currentItemIndex >= totalItemCount - 1;
  if (currentItemIndex >= totalItemCount - 1) {
    nextItemButton.classList.add(...navigationClasses);
  } else {
    nextItemButton.classList.remove(...navigationClasses);
  }
}

async function saveCurrentDistribution(): Promise<void> {
  if (selectedPersons.length === 0 || !currentItem) {
    return;
  }

  try {
    const response = await fetch("/save_distribution", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        item_index: getItemIndexFromUrl(),
        person_ids: selectedPersons,
        item_name: currentItem.name,
        item_price: currentItem.price,
      }),
    });

    if (!response.ok) {
      console.error("Failed to save distribution");
    }
  } catch (error) {
    console.error("Error saving distribution:", error);
  }
}

async function handleBack(): Promise<void> {
  await saveCurrentDistribution();
  window.location.href = "/items";
}

async function handleDone(): Promise<void> {
  await saveCurrentDistribution();
  loadingOverlay.classList.remove("hidden");
  window.location.href = "/extras";
}

function getItemIndexFromUrl(): number {
  const urlParams = new URLSearchParams(window.location.search);
  return parseInt(urlParams.get("item_index") || "0");
}

// Helper to fetch initial data from meta tags or window context
function initializePersonData(): void {
  const personCountElement = document.getElementById("person-count") as HTMLMetaElement;
  const personIndexElement = document.getElementById("person-index") as HTMLMetaElement;
  totalPersonCount = parseInt(personCountElement.content || "0");
  currentPersonIndex = parseInt(personIndexElement.content || "0");
}

// Fetch all persons and items from backend
async function fetchDistributeData() {
  const [personsRes, itemsRes] = await Promise.all([
    fetch("/get_persons"),
    fetch("/get_items"),
  ]);
  persons = await personsRes.json();
  items = await itemsRes.json();
}

// Render all items for the current person
function renderItemsForPerson() {
  const person = persons[currentPersonIndex];
  personName.textContent = person.name;
  const itemsList = document.querySelectorAll(".item-box");
  itemsList.forEach((itemBox, idx) => {
    const itemIndex = parseInt((itemBox as HTMLElement).getAttribute("data-item-index") || "0");
    if (person.items.includes(itemIndex)) {
      itemBox.classList.add("ring-4", "ring-green-400/40", "border-green-400");
    } else {
      itemBox.classList.remove("ring-4", "ring-green-400/40", "border-green-400");
    }
    // Update amount for this item for this person
    const amountDiv = itemBox.querySelector(".text-blue-400.font-semibold") as HTMLElement;
    const share = getPersonItemShare(itemIndex, person);
    amountDiv.textContent = `$${share.toFixed(2)}`;
  });
}

// Calculate share for a person for an item
function getPersonItemShare(itemIndex: number, person: any): number {
  const item = items[itemIndex];
  // Count how many persons have this item
  const count = persons.filter(p => p.items.includes(itemIndex)).length;
  if (person.items.includes(itemIndex) && count > 0) {
    return item.price / count;
  }
  return 0;
}

// Toggle item for current person
async function handleItemBoxClick(e: Event) {
  const itemBox = e.currentTarget as HTMLElement;
  const itemIndex = parseInt(itemBox.getAttribute("data-item-index") || "0");
  const person = persons[currentPersonIndex];
  const hasItem = person.items.includes(itemIndex);
  // Update backend
  await fetch("/save_distribution", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      person_index: currentPersonIndex,
      item_index: itemIndex,
      add: !hasItem
    })
  });
  // Update local state
  if (hasItem) {
    person.items = person.items.filter((idx: number) => idx !== itemIndex);
  } else {
    person.items.push(itemIndex);
  }
  renderItemsForPerson();
}

// Navigation
function updateNavigationButtons() {
  prevPersonButton.disabled = currentPersonIndex <= 0;
  nextPersonButton.disabled = currentPersonIndex >= totalPersonCount - 1;
}

async function handlePrevPerson() {
  if (currentPersonIndex > 0) {
    currentPersonIndex--;
    renderItemsForPerson();
    updateNavigationButtons();
  }
}
async function handleNextPerson() {
  if (currentPersonIndex < totalPersonCount - 1) {
    currentPersonIndex++;
    renderItemsForPerson();
    updateNavigationButtons();
  }
}
