// State management
let currentEditIndex: number = -1;
let isAddMode: boolean = false;

// DOM elements
const itemsListView = document.getElementById('items-list-view') as HTMLDivElement;
const editItemView = document.getElementById('edit-item-view') as HTMLDivElement;
const editItemForm = document.getElementById('edit-item-form') as HTMLFormElement;
const editItemIndex = document.getElementById('edit-item-index') as HTMLInputElement;
const editItemName = document.getElementById('edit-item-name') as HTMLInputElement;
const editItemPrice = document.getElementById('edit-item-price') as HTMLInputElement;
const cancelButton = document.getElementById('cancel-button') as HTMLButtonElement;
const splitButton = document.getElementById('split-button') as HTMLButtonElement;
const saveButton = document.getElementById('save-button') as HTMLButtonElement;
const addItemButton = document.getElementById('add-item-button') as HTMLButtonElement;
const editTitle = document.getElementById('edit-title') as HTMLHeadingElement;
const editSubtitle = document.getElementById('edit-subtitle') as HTMLParagraphElement;

// Show the items list view
function showItemsList(): void {
    itemsListView.classList.remove('hidden');
    editItemView.classList.add('hidden');
    currentEditIndex = -1;
    isAddMode = false;
}

// Show the edit item view for editing
function showEditItem(index: number, name: string, price: number): void {
    currentEditIndex = index;
    isAddMode = false;
    editItemIndex.value = index.toString();
    editItemName.value = name;
    editItemPrice.value = price.toFixed(2);
    
    // Update UI for edit mode
    editTitle.textContent = 'Edit Item';
    editSubtitle.textContent = 'Modify item details';
    splitButton.classList.remove('hidden');
    
    itemsListView.classList.add('hidden');
    editItemView.classList.remove('hidden');
    
    // Focus on the name input
    editItemName.focus();
}

// Show the edit item view for adding
function showAddItem(): void {
    currentEditIndex = -1;
    isAddMode = true;
    editItemIndex.value = '';
    editItemName.value = '';
    editItemPrice.value = '';
    
    // Update UI for add mode
    editTitle.textContent = 'Add Item';
    editSubtitle.textContent = 'Create a new item';
    splitButton.classList.add('hidden');
    
    itemsListView.classList.add('hidden');
    editItemView.classList.remove('hidden');
    
    // Focus on the name input
    editItemName.focus();
}

// Handle item click to enter edit mode
function setupItemClickHandlers(): void {
    const itemElements = document.querySelectorAll('[data-item-index]');
    itemElements.forEach((element) => {
        element.addEventListener('click', () => {
            const index = parseInt(element.getAttribute('data-item-index') || '0');
            const name = element.getAttribute('data-item-name') || '';
            const price = parseFloat(element.getAttribute('data-item-price') || '0');
            showEditItem(index, name, price);
        });
    });
}

// Cancel button - return to list view
function handleCancel(): void {
    showItemsList();
}

// Split button - split the current item
async function handleSplit(): Promise<void> {
    if (currentEditIndex === -1 || isAddMode) return;
    
    try {
        const response = await fetch('/split_item', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                item_index: currentEditIndex
            })
        });
        
        if (response.ok) {
            // Reload the page to show updated items
            window.location.reload();
        } else {
            console.error('Failed to split item');
        }
    } catch (error) {
        console.error('Error splitting item:', error);
    }
}

// Save button - update the current item or add new item
async function handleSave(): Promise<void> {
    const name = editItemName.value.trim();
    const price = parseFloat(editItemPrice.value);
    
    if (!name || isNaN(price) || price < 0) {
        alert('Please enter a valid name and price');
        return;
    }
    
    try {
        const endpoint = isAddMode ? '/add_item' : '/update_item';
        const body = isAddMode 
            ? { name: name, price: price }
            : { item_index: currentEditIndex, name: name, price: price };
        
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body)
        });
        
        if (response.ok) {
            // Reload the page to show updated items
            window.location.reload();
        } else {
            console.error(`Failed to ${isAddMode ? 'add' : 'update'} item`);
        }
    } catch (error) {
        console.error(`Error ${isAddMode ? 'adding' : 'updating'} item:`, error);
    }
}

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    // Setup event listeners
    cancelButton.addEventListener('click', handleCancel);
    splitButton.addEventListener('click', handleSplit);
    saveButton.addEventListener('click', handleSave);
    addItemButton.addEventListener('click', showAddItem);
    
    // Setup item click handlers
    setupItemClickHandlers();
    
    // Handle form submission (for the save button)
    editItemForm.addEventListener('submit', (e) => {
        e.preventDefault();
        handleSave();
    });
    
    // Handle Enter key in inputs
    editItemName.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            editItemPrice.focus();
        }
    });
    
    editItemPrice.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            handleSave();
        }
    });
    
    // Handle Escape key to cancel
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !editItemView.classList.contains('hidden')) {
            handleCancel();
        }
    });
});
