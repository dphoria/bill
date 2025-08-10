let currentPersonIndex: number = 0;
let totalPersonCount: number = 0;

const personName = document.getElementById("person-name") as HTMLSpanElement;
const personTotal = document.getElementById("person-total") as HTMLSpanElement;
const prevPersonButton = document.getElementById(
  "prev-person-button",
) as HTMLButtonElement;
const nextPersonButton = document.getElementById(
  "next-person-button",
) as HTMLButtonElement;
const extrasButton = document.getElementById(
  "extras-button",
) as HTMLButtonElement;
const downloadButton = document.getElementById(
  "download-button",
) as HTMLButtonElement;

document.addEventListener("DOMContentLoaded", () => {
  prevPersonButton.addEventListener("click", handlePrevPerson);
  nextPersonButton.addEventListener("click", handleNextPerson);
  extrasButton.addEventListener("click", handleExtras);
  downloadButton.addEventListener("click", handleDownload);

  initializePersonData();
  setupItemClickedHandlers();

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      handleExtras();
    }
  });
});

function initializePersonData(): void {
  const personCountElement = document.getElementById(
    "person-count",
  ) as HTMLMetaElement;
  const personIndexElement = document.getElementById(
    "person-index",
  ) as HTMLMetaElement;

  totalPersonCount = parseInt(personCountElement.content || "0");
  currentPersonIndex = parseInt(personIndexElement.content || "0");
}

function handlePrevPerson(): void {
  if (currentPersonIndex > 0) {
    currentPersonIndex--;
    navigateToPerson(currentPersonIndex);
  }
}

function handleNextPerson(): void {
  if (currentPersonIndex < totalPersonCount - 1) {
    currentPersonIndex++;
    navigateToPerson(currentPersonIndex);
  }
}

function navigateToPerson(personIndex: number): void {
  const url = new URL(window.location.href);
  url.searchParams.set("person_index", personIndex.toString());
  window.location.href = url.toString();
}

function handleExtras(): void {
  window.location.href = "/extras";
}

function handleDownload(): void {
  window.location.href = "/payments/download";
}

function setupItemClickedHandlers(): void {
  const itemElements = document.querySelectorAll(".item-box");
  itemElements.forEach((itemElement) => {
    itemElement.addEventListener("click", handleItemClick);
  });
}

async function handleItemClick(e: Event): Promise<void> {
  const itemElement = e.currentTarget as HTMLElement;
  const itemIndex = parseInt(itemElement.getAttribute("data-item-index") || "0");
  
  try {
    const response = await fetch("/share_item", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        item_index: itemIndex,
        person_index: currentPersonIndex,
      }),
    });

    if (response.ok) {
      const result = await response.json();
      updateItemInfoDisplay(itemElement, result);
    }
  } catch (error) {
    console.error("Error sharing item:", error);
  }
}

function updateItemInfoDisplay(itemElement: HTMLElement, data: any): void {
  const shareElement = itemElement.querySelector(".text-blue-400.font-semibold") as HTMLElement;
  const priceElement = itemElement.querySelector(".text-xs.text-slate-400") as HTMLElement;
  
  if (data.share !== undefined) {
    shareElement.textContent = `$${data.share.toFixed(2)}`;
  }
  
  if (data.share > 0) {
    itemElement.classList.add("ring-4", "ring-green-400/40", "border-green-400");
  } else {
    itemElement.classList.remove("ring-4", "ring-green-400/40", "border-green-400");
  }
  
  if (data.person_subtotal !== undefined) {
    const subtotalElement = document.querySelector(".text-green-400") as HTMLElement;
    if (subtotalElement) {
      subtotalElement.textContent = `$${data.person_subtotal.toFixed(2)}`;
    }
  }
  
  if (data.person_total !== undefined) {
    const totalElement = document.getElementById("person-total") as HTMLElement;
    if (totalElement) {
      totalElement.textContent = `$${data.person_total.toFixed(2)}`;
    }
  }
}
