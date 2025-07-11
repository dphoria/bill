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

document.addEventListener("DOMContentLoaded", () => {
  prevPersonButton.addEventListener("click", handlePrevPerson);
  nextPersonButton.addEventListener("click", handleNextPerson);
  extrasButton.addEventListener("click", handleExtras);

  initializePersonData();

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
