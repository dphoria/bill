interface Person {
  name: string;
  items: string[];
}

let persons: Person[] = [];

document.addEventListener("DOMContentLoaded", function (): void {
  const nameInput = document.getElementById("name") as HTMLInputElement;
  const doneBtn = document.getElementById("done-btn") as HTMLButtonElement;
  const personsList = document.getElementById("persons-list") as HTMLElement;

  initializePersonsFromDOM();

  function initializePersonsFromDOM(): void {
    if (personsList) {
      const personElements = personsList.querySelectorAll("[id^='person-']");
      persons = Array.from(personElements).map((element, index) => ({
        name:
          (element.querySelector(".font-medium") as HTMLElement)?.textContent ||
          "",
        items: [],
      }));
    }
  }

  function updateDoneButton(): void {
    const nameEmpty: boolean = !nameInput.value.trim();
    const personsEmpty: boolean = persons.length === 0;

    if (nameEmpty && personsEmpty) {
      doneBtn.disabled = true;
    } else {
      doneBtn.disabled = false;
    }
  }

  updateDoneButton();

  nameInput.addEventListener("input", updateDoneButton);
});
