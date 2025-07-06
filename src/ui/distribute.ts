// State management
let selectedPersons: number[] = [];
let currentItem: { name: string; price: number } | null = null;
let currentItemIndex: number = 0;
let totalItemCount: number = 0;

// DOM elements
const itemName = document.getElementById('item-name') as HTMLSpanElement;
const itemPrice = document.getElementById('item-price') as HTMLSpanElement;
const prevItemButton = document.getElementById('prev-item-button') as HTMLButtonElement;
const nextItemButton = document.getElementById('next-item-button') as HTMLButtonElement;
const backButton = document.getElementById('back-button') as HTMLButtonElement;
const distributeButton = document.getElementById('distribute-button') as HTMLButtonElement;
const distributionResults = document.getElementById('distribution-results') as HTMLDivElement;
const resultsList = document.getElementById('results-list') as HTMLDivElement;

// Initialize the page
document.addEventListener('DOMContentLoaded', async () => {
    // Setup event listeners
    prevItemButton.addEventListener('click', handlePrevItem);
    nextItemButton.addEventListener('click', handleNextItem);
    backButton.addEventListener('click', handleBack);
    distributeButton.addEventListener('click', handleDone);
    
    // Initialize item data from template (includes item data)
    initializeItemData();
    
    // Setup person selection handlers (item data is now available)
    setupPersonSelectionHandlers();
    
    // Handle Escape key to go back
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            handleBack();
        }
    });
});

// Setup person selection handlers
function setupPersonSelectionHandlers(): void {
    // Clear any existing selections
    selectedPersons = [];
    
    const personElements = document.querySelectorAll('.person-box');
    personElements.forEach((element) => {
        const personId = parseInt(element.getAttribute('data-person-id') || '0');
        const isSelected = element.getAttribute('data-selected') === 'true';
        
        // Initialize selectedPersons based on data-selected attribute
        if (isSelected) {
            selectedPersons.push(personId);
            element.classList.add('bg-green-600/30', 'border-green-400', 'border-2', 'ring-4', 'ring-green-400/40', 'shadow-lg');
        }
        
        // Add click event listener to the person box
        element.addEventListener('click', (e) => {
            console.log('Person box clicked:', personId); // Debug log
            
            const isCurrentlySelected = selectedPersons.includes(personId);
            console.log('Currently selected:', isCurrentlySelected); // Debug log
            
            if (isCurrentlySelected) {
                // Remove from selection
                selectedPersons = selectedPersons.filter(id => id !== personId);
                element.classList.remove('bg-green-600/30', 'border-green-400', 'border-2', 'ring-4', 'ring-green-400/40', 'shadow-lg');
                element.setAttribute('data-selected', 'false');
                console.log('Removed from selection'); // Debug log
            } else {
                // Add to selection
                selectedPersons.push(personId);
                element.classList.add('bg-green-600/30', 'border-green-400', 'border-2', 'ring-4', 'ring-green-400/40', 'shadow-lg');
                element.setAttribute('data-selected', 'true');
                console.log('Added to selection'); // Debug log
            }
            
            console.log('Selected persons:', selectedPersons); // Debug log
            updateDistributeButton();
        });
    });
    
    // Update the UI after initializing selectedPersons
    updateDistributeButton();
}

// Initialize item data from template variables
function initializeItemData(): void {
    // Get item count and current index from template variables
    const itemCountElement = document.getElementById('item-count') as HTMLMetaElement;
    const itemIndexElement = document.getElementById('item-index') as HTMLMetaElement;
    const itemNameElement = document.getElementById('item-name') as HTMLMetaElement;
    const itemPriceElement = document.getElementById('item-price') as HTMLMetaElement;
    
    if (itemCountElement) {
        totalItemCount = parseInt(itemCountElement.content || '0');
    }
    
    if (itemIndexElement) {
        currentItemIndex = parseInt(itemIndexElement.content || '0');
    }
    
    // Get current item data from template
    if (itemNameElement && itemPriceElement) {
        const itemName = itemNameElement.content || '';
        const itemPrice = parseFloat(itemPriceElement.content || '0');
        
        if (itemName && itemPrice > 0) {
            currentItem = {
                name: itemName,
                price: itemPrice
            };
        }
    }
    
    // Update navigation buttons
    updateNavigationButtons();
}

// Get current item from URL parameters or session
async function getCurrentItem(): Promise<void> {
    const urlParams = new URLSearchParams(window.location.search);
    const itemIndex = urlParams.get('item_index');
    
    if (itemIndex) {
        try {
            const response = await fetch(`/get_item?item_index=${itemIndex}`);
            if (response.ok) {
                const item = await response.json();
                currentItem = item;
                updateItemDisplay();
            }
        } catch (error) {
            console.error('Error fetching item:', error);
        }
    }
}

// Update item display
function updateItemDisplay(): void {
    if (currentItem) {
        itemName.textContent = currentItem.name;
        itemPrice.textContent = `$${currentItem.price.toFixed(2)}`;
    }
}

// Update distribute button state and calculate shares
function updateDistributeButton(): void {
    distributeButton.disabled = selectedPersons.length === 0;
    if (selectedPersons.length === 0) {
        distributeButton.classList.add('opacity-50', 'cursor-not-allowed');
        // Reset all person shares to $0.00
        document.querySelectorAll('.person-share').forEach((element) => {
            (element as HTMLSpanElement).textContent = '$0.00';
        });
    } else {
        distributeButton.classList.remove('opacity-50', 'cursor-not-allowed');
        // Calculate and update shares
        updatePersonShares();
    }
}

// Calculate and update person shares
function updatePersonShares(): void {
    if (!currentItem || selectedPersons.length === 0) return;
    
    const sharePerPerson = currentItem.price / selectedPersons.length;
    
    // Reset all shares to $0.00 first
    document.querySelectorAll('.person-share').forEach((element) => {
        (element as HTMLSpanElement).textContent = '$0.00';
    });
    
    // Update shares for selected persons
    selectedPersons.forEach((personId) => {
        const shareElement = document.querySelector(`.person-share[data-person-id="${personId}"]`) as HTMLSpanElement;
        if (shareElement) {
            shareElement.textContent = `$${sharePerPerson.toFixed(2)}`;
        }
    });
}

// Handle previous item button
async function handlePrevItem(): Promise<void> {
    if (currentItemIndex > 0) {
        // Save current distribution before navigating
        await saveCurrentDistribution();
        window.location.href = `/distribute?item_index=${currentItemIndex - 1}`;
    }
}

// Handle next item button
async function handleNextItem(): Promise<void> {
    if (currentItemIndex < totalItemCount - 1) {
        // Save current distribution before navigating
        await saveCurrentDistribution();
        window.location.href = `/distribute?item_index=${currentItemIndex + 1}`;
    }
}

// Update navigation button states
function updateNavigationButtons(): void {
    if (prevItemButton) {
        prevItemButton.disabled = currentItemIndex <= 0;
        if (currentItemIndex <= 0) {
            prevItemButton.classList.add('opacity-50', 'cursor-not-allowed');
        } else {
            prevItemButton.classList.remove('opacity-50', 'cursor-not-allowed');
        }
    }
    
    if (nextItemButton) {
        nextItemButton.disabled = currentItemIndex >= totalItemCount - 1;
        if (currentItemIndex >= totalItemCount - 1) {
            nextItemButton.classList.add('opacity-50', 'cursor-not-allowed');
        } else {
            nextItemButton.classList.remove('opacity-50', 'cursor-not-allowed');
        }
    }
}

// Save current distribution to session data
async function saveCurrentDistribution(): Promise<void> {
    if (selectedPersons.length === 0 || !currentItem) {
        return; // Nothing to save
    }
    
    try {
        const response = await fetch('/save_distribution', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                item_index: getItemIndexFromUrl(),
                person_ids: selectedPersons,
                item_name: currentItem.name,
                item_price: currentItem.price
            })
        });
        
        if (!response.ok) {
            console.error('Failed to save distribution');
        }
    } catch (error) {
        console.error('Error saving distribution:', error);
    }
}

// Handle back button (Items)
async function handleBack(): Promise<void> {
    // Save current distribution before navigating
    await saveCurrentDistribution();
    window.location.href = '/items';
}

// Handle done button - navigate to extras page
async function handleDone(): Promise<void> {
    // Save current distribution before proceeding
    await saveCurrentDistribution();
    window.location.href = '/extras';
}



// Get item index from URL parameters
function getItemIndexFromUrl(): number {
    const urlParams = new URLSearchParams(window.location.search);
    return parseInt(urlParams.get('item_index') || '0');
}

// Show distribution results
function showDistributionResults(result: any): void {
    resultsList.innerHTML = '';
    
    if (result.distribution) {
        result.distribution.forEach((personShare: any) => {
            const resultElement = document.createElement('div');
            resultElement.className = 'flex justify-between items-center p-3 bg-slate-800/50 rounded-lg border border-slate-700';
            resultElement.innerHTML = `
                <span class="font-medium text-slate-100">${personShare.person_name}</span>
                <span class="text-green-400 font-semibold">$${personShare.share.toFixed(2)}</span>
            `;
            resultsList.appendChild(resultElement);
        });
        
        // Show total
        const totalElement = document.createElement('div');
        totalElement.className = 'flex justify-between items-center p-3 bg-slate-700/50 rounded-lg border border-slate-600 mt-2';
        totalElement.innerHTML = `
            <span class="font-semibold text-slate-200">Total Distributed:</span>
            <span class="text-blue-400 font-semibold">$${result.total_distributed.toFixed(2)}</span>
        `;
        resultsList.appendChild(totalElement);
        
        // Show remainder if any
        if (result.remainder && result.remainder > 0) {
            const remainderElement = document.createElement('div');
            remainderElement.className = 'flex justify-between items-center p-3 bg-orange-900/30 rounded-lg border border-orange-700 mt-2';
            remainderElement.innerHTML = `
                <span class="font-medium text-orange-300">Remainder:</span>
                <span class="text-orange-400 font-semibold">$${result.remainder.toFixed(2)}</span>
            `;
            resultsList.appendChild(remainderElement);
        }
    }
    
    distributionResults.classList.remove('hidden');
    
    // Scroll to results
    distributionResults.scrollIntoView({ behavior: 'smooth' });
} 