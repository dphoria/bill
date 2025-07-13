let selectedPersons: number[] = [];
let currentItem: { name: string; price: number } | null = null;
let currentItemIndex: number = 0;
let totalItemCount: number = 0;

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

document.addEventListener("DOMContentLoaded", async () => {
  prevItemButton.addEventListener("click", handlePrevItem);
  nextItemButton.addEventListener("click", handleNextItem);
  backButton.addEventListener("click", handleBack);
  distributeButton.addEventListener("click", handleDone);

  initializeItemData();

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

  const personElements = document.querySelectorAll(".person-box");
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
  const itemNameElement = document.getElementById(
    "item-name",
  ) as HTMLMetaElement;
  const itemPriceElement = document.getElementById(
    "item-price",
  ) as HTMLMetaElement;

  totalItemCount = parseInt(itemCountElement.content || "0");
  currentItemIndex = parseInt(itemIndexElement.content || "0");

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
  window.location.href = "/extras";
}

function getItemIndexFromUrl(): number {
  const urlParams = new URLSearchParams(window.location.search);
  return parseInt(urlParams.get("item_index") || "0");
}
