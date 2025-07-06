interface Person {
  name: string;
  items: string[];
}

let persons: Person[] = [];

document.addEventListener('DOMContentLoaded', function(): void {
  const nameInput = document.getElementById('name') as HTMLInputElement;
  const doneBtn = document.getElementById('done-btn') as HTMLButtonElement;
  const personsList = document.querySelector('.space-y-2') as HTMLElement;
  
  // Initialize persons array from the DOM
  initializePersonsFromDOM();
  
  function initializePersonsFromDOM(): void {
    if (personsList) {
      const personElements = personsList.querySelectorAll('.flex.items-center.justify-between');
      persons = Array.from(personElements).map((element, index) => ({
        name: (element.querySelector('.font-medium') as HTMLElement)?.textContent || '',
        items: []
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
  
  // Check on page load
  updateDoneButton();
  
  // Check when input changes
  nameInput.addEventListener('input', updateDoneButton);
}); 