"use strict";
// State management
class ReceiptManager {
    constructor() {
        this.state = {
            items: [],
            people: [],
            taxPercent: 10.35,
            tipPercent: 20
        };
        this.subscribers = [];
    }
    // Getters
    getItems() {
        return [...this.state.items];
    }
    getPeople() {
        return [...this.state.people];
    }
    getTaxPercent() {
        return this.state.taxPercent;
    }
    getTipPercent() {
        return this.state.tipPercent;
    }
    // Actions
    addItem(name, price) {
        const item = {
            id: crypto.randomUUID(),
            name: name.trim(),
            price: parseFloat(price.toString())
        };
        this.state.items.push(item);
        this.notifySubscribers();
    }
    updateItem(id, name, price) {
        const item = this.state.items.find(item => item.id === id);
        if (item) {
            item.name = name.trim();
            item.price = parseFloat(price.toString());
            this.notifySubscribers();
        }
    }
    deleteItem(id) {
        this.state.items = this.state.items.filter(item => item.id !== id);
        // Remove item from all people's selections
        this.state.people.forEach(person => {
            person.selectedItems = person.selectedItems.filter(itemId => itemId !== id);
        });
        this.notifySubscribers();
    }
    addPerson(name) {
        const person = {
            id: crypto.randomUUID(),
            name: name.trim(),
            selectedItems: []
        };
        this.state.people.push(person);
        this.notifySubscribers();
    }
    removePerson(id) {
        this.state.people = this.state.people.filter(person => person.id !== id);
        this.notifySubscribers();
    }
    toggleItemForPerson(personId, itemId) {
        const person = this.state.people.find(p => p.id === personId);
        if (person) {
            const index = person.selectedItems.indexOf(itemId);
            if (index > -1) {
                person.selectedItems.splice(index, 1);
            }
            else {
                person.selectedItems.push(itemId);
            }
            this.notifySubscribers();
        }
    }
    updateTaxPercent(percent) {
        this.state.taxPercent = percent;
        this.notifySubscribers();
    }
    updateTipPercent(percent) {
        this.state.tipPercent = percent;
        this.notifySubscribers();
    }
    // Calculations
    calculateSubtotal() {
        return this.state.items.reduce((sum, item) => sum + item.price, 0);
    }
    calculateTax() {
        return this.calculateSubtotal() * (this.state.taxPercent / 100);
    }
    calculateTip() {
        return this.calculateSubtotal() * (this.state.tipPercent / 100);
    }
    calculateTotal() {
        return this.calculateSubtotal() + this.calculateTax() + this.calculateTip();
    }
    calculatePersonTotal(person) {
        let subtotal = 0;
        person.selectedItems.forEach(itemId => {
            const item = this.state.items.find(i => i.id === itemId);
            if (item) {
                const numPeopleSharing = this.getNumPeopleForItem(itemId);
                if (numPeopleSharing > 0) {
                    subtotal += item.price / numPeopleSharing;
                }
            }
        });
        const tax = subtotal * (this.state.taxPercent / 100);
        const tip = subtotal * (this.state.tipPercent / 100);
        const total = subtotal + tax + tip;
        return { subtotal, tax, tip, total };
    }
    getNumPeopleForItem(itemId) {
        return this.state.people.filter(person => person.selectedItems.includes(itemId)).length;
    }
    // Subscription system
    subscribe(callback) {
        this.subscribers.push(callback);
        return () => {
            const index = this.subscribers.indexOf(callback);
            if (index > -1) {
                this.subscribers.splice(index, 1);
            }
        };
    }
    notifySubscribers() {
        this.subscribers.forEach(callback => callback());
    }
}
// UI Components
class ModernUI {
    constructor() {
        this.elements = {};
        this.manager = new ReceiptManager();
        this.initializeElements();
        this.setupEventListeners();
        this.subscribeToState();
    }
    initializeElements() {
        const selectors = {
            'itemsTable': '#receipt-table tbody',
            'subtotal': '#subtotal',
            'tax': '#tax',
            'tip': '#tip',
            'total': '#total',
            'taxPercent': '#tax-percent',
            'tipPercent': '#tip-percent',
            'peopleList': '#people-list',
            'addItemModal': '#add-item-modal',
            'addPersonModal': '#add-person-modal',
            'editPercentageModal': '#edit-percentage-modal',
            'addItemForm': '#add-item-form',
            'addPersonForm': '#add-person-form',
            'editPercentageForm': '#edit-percentage-form',
            'itemName': '#item-name',
            'itemPrice': '#item-price',
            'itemIndex': '#item-index',
            'personName': '#person-name',
            'percentageValue': '#percentage-value',
            'percentageType': '#percentage-type',
            'editPercentageTitle': '#edit-percentage-title'
        };
        Object.entries(selectors).forEach(([key, selector]) => {
            this.elements[key] = document.querySelector(selector);
        });
    }
    setupEventListeners() {
        var _a, _b, _c, _d, _e, _f, _g, _h, _j, _k;
        // Form submissions
        (_a = this.elements.addItemForm) === null || _a === void 0 ? void 0 : _a.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleAddItem();
        });
        (_b = this.elements.addPersonForm) === null || _b === void 0 ? void 0 : _b.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleAddPerson();
        });
        (_c = this.elements.editPercentageForm) === null || _c === void 0 ? void 0 : _c.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleEditPercentage();
        });
        // Modal cancel buttons
        (_d = document.getElementById('add-item-cancel')) === null || _d === void 0 ? void 0 : _d.addEventListener('click', () => {
            this.hideModal('add-item-modal');
        });
        (_e = document.getElementById('add-person-cancel')) === null || _e === void 0 ? void 0 : _e.addEventListener('click', () => {
            this.hideModal('add-person-modal');
        });
        (_f = document.getElementById('edit-percentage-cancel')) === null || _f === void 0 ? void 0 : _f.addEventListener('click', () => {
            this.hideModal('edit-percentage-modal');
        });
        // Action buttons
        (_g = document.getElementById('add-item-button')) === null || _g === void 0 ? void 0 : _g.addEventListener('click', () => {
            this.showAddItemModal();
        });
        (_h = document.getElementById('add-person-button')) === null || _h === void 0 ? void 0 : _h.addEventListener('click', () => {
            this.showModal('add-person-modal');
        });
        (_j = document.getElementById('tax-button')) === null || _j === void 0 ? void 0 : _j.addEventListener('click', () => {
            this.showPercentageModal('tax');
        });
        (_k = document.getElementById('tip-button')) === null || _k === void 0 ? void 0 : _k.addEventListener('click', () => {
            this.showPercentageModal('tip');
        });
        // Close modals when clicking outside
        document.querySelectorAll('[id$="-modal"]').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.hideModal(modal.id);
                }
            });
        });
    }
    subscribeToState() {
        this.manager.subscribe(() => {
            this.render();
        });
    }
    render() {
        this.renderItemsTable();
        this.renderSummary();
        this.renderPeopleList();
    }
    renderItemsTable() {
        const tbody = this.elements.itemsTable;
        if (!tbody)
            return;
        tbody.innerHTML = '';
        this.manager.getItems().forEach((item, index) => {
            const row = document.createElement('tr');
            row.className = 'border-b border-dark-800 hover:bg-dark-800/50 transition-colors';
            row.innerHTML = `
        <td class="py-4 px-4">
          <button onclick="modernUI.editItem('${item.id}')" class="text-left text-white hover:text-primary-400 transition-colors font-medium">
            ${item.name}
          </button>
        </td>
        <td class="py-4 px-4 text-right text-white font-mono">
          $${item.price.toFixed(2)}
        </td>
        <td class="py-4 px-2">
          <button onclick="modernUI.deleteItem('${item.id}')" class="text-dark-400 hover:text-accent-400 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
            </svg>
          </button>
        </td>
      `;
            tbody.appendChild(row);
        });
    }
    renderSummary() {
        const subtotal = this.manager.calculateSubtotal();
        const tax = this.manager.calculateTax();
        const tip = this.manager.calculateTip();
        const total = this.manager.calculateTotal();
        if (this.elements.subtotal) {
            this.elements.subtotal.textContent = `$${subtotal.toFixed(2)}`;
        }
        if (this.elements.tax) {
            this.elements.tax.textContent = `$${tax.toFixed(2)}`;
        }
        if (this.elements.tip) {
            this.elements.tip.textContent = `$${tip.toFixed(2)}`;
        }
        if (this.elements.total) {
            this.elements.total.textContent = `$${total.toFixed(2)}`;
        }
        if (this.elements.taxPercent) {
            this.elements.taxPercent.textContent = `(${this.manager.getTaxPercent()}%)`;
        }
        if (this.elements.tipPercent) {
            this.elements.tipPercent.textContent = `(${this.manager.getTipPercent()}%)`;
        }
    }
    renderPeopleList() {
        const peopleList = this.elements.peopleList;
        if (!peopleList)
            return;
        const people = this.manager.getPeople();
        if (people.length === 0) {
            peopleList.innerHTML = `
        <div class="text-center py-8 text-dark-400">
          <svg class="w-12 h-12 mx-auto mb-3 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"></path>
          </svg>
          <p>No people added yet</p>
          <p class="text-sm">Add people to split the bill</p>
        </div>
      `;
            return;
        }
        peopleList.innerHTML = '';
        people.forEach(person => {
            const personTotal = this.manager.calculatePersonTotal(person);
            const personElement = document.createElement('div');
            personElement.className = 'card p-4';
            personElement.innerHTML = `
        <div class="flex justify-between items-start mb-3">
          <div>
            <h4 class="font-semibold text-white">${person.name}</h4>
            <p class="text-sm text-dark-400">${person.selectedItems.length} items selected</p>
          </div>
          <button onclick="modernUI.removePerson('${person.id}')" class="text-dark-400 hover:text-accent-400 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <div class="space-y-2 text-sm">
          <div class="flex justify-between">
            <span class="text-dark-300">Subtotal:</span>
            <span class="text-white font-mono">$${personTotal.subtotal.toFixed(2)}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-dark-300">Tax:</span>
            <span class="text-white font-mono">$${personTotal.tax.toFixed(2)}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-dark-300">Tip:</span>
            <span class="text-white font-mono">$${personTotal.tip.toFixed(2)}</span>
          </div>
          <div class="flex justify-between pt-2 border-t border-dark-700">
            <span class="font-semibold text-white">Total:</span>
            <span class="font-semibold text-primary-400 font-mono">$${personTotal.total.toFixed(2)}</span>
          </div>
        </div>
        
        <div class="mt-4">
          <h5 class="text-sm font-medium text-dark-300 mb-2">Selected Items:</h5>
          <div class="space-y-1">
            ${person.selectedItems.map(itemId => {
                const item = this.manager.getItems().find(i => i.id === itemId);
                if (!item)
                    return '';
                const numPeople = this.manager.getNumPeopleForItem(itemId);
                const share = numPeople > 0 ? item.price / numPeople : 0;
                return `
                <div class="flex justify-between text-xs">
                  <span class="text-dark-400">${item.name}</span>
                  <span class="text-white font-mono">$${share.toFixed(2)}</span>
                </div>
              `;
            }).join('')}
          </div>
        </div>
      `;
            peopleList.appendChild(personElement);
        });
    }
    // Modal management
    showModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('hidden');
            modal.classList.add('flex');
            const firstInput = modal.querySelector('input');
            if (firstInput) {
                firstInput.focus();
            }
        }
    }
    hideModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('hidden');
            modal.classList.remove('flex');
            const form = modal.querySelector('form');
            if (form) {
                form.reset();
            }
        }
    }
    showAddItemModal(itemId) {
        if (itemId) {
            const item = this.manager.getItems().find(i => i.id === itemId);
            if (item) {
                this.elements.itemName.value = item.name;
                this.elements.itemPrice.value = item.price.toString();
                this.elements.itemIndex.value = itemId;
            }
        }
        else {
            this.elements.itemIndex.value = '';
            this.elements.itemName.value = '';
            this.elements.itemPrice.value = '0.00';
        }
        this.showModal('add-item-modal');
    }
    showPercentageModal(type) {
        const value = type === 'tax' ? this.manager.getTaxPercent() : this.manager.getTipPercent();
        const title = type === 'tax' ? 'Edit Tax Rate' : 'Edit Tip Rate';
        this.elements.percentageValue.value = value.toString();
        this.elements.percentageType.value = type;
        this.elements.editPercentageTitle.textContent = title;
        this.showModal('edit-percentage-modal');
    }
    // Event handlers
    handleAddItem() {
        const name = this.elements.itemName.value.trim();
        const price = parseFloat(this.elements.itemPrice.value);
        const itemId = this.elements.itemIndex.value;
        if (!name || isNaN(price) || price < 0) {
            alert('Please enter valid item name and price');
            return;
        }
        if (itemId) {
            this.manager.updateItem(itemId, name, price);
        }
        else {
            this.manager.addItem(name, price);
        }
        this.hideModal('add-item-modal');
    }
    handleAddPerson() {
        const name = this.elements.personName.value.trim();
        if (!name) {
            alert('Please enter a name');
            return;
        }
        this.manager.addPerson(name);
        this.hideModal('add-person-modal');
    }
    handleEditPercentage() {
        const value = parseFloat(this.elements.percentageValue.value);
        const type = this.elements.percentageType.value;
        if (isNaN(value) || value < 0 || value > 100) {
            alert('Please enter a valid percentage between 0 and 100');
            return;
        }
        if (type === 'tax') {
            this.manager.updateTaxPercent(value);
        }
        else {
            this.manager.updateTipPercent(value);
        }
        this.hideModal('edit-percentage-modal');
    }
    // Public methods for onclick handlers
    editItem(itemId) {
        this.showAddItemModal(itemId);
    }
    deleteItem(itemId) {
        if (confirm('Are you sure you want to delete this item?')) {
            this.manager.deleteItem(itemId);
        }
    }
    removePerson(personId) {
        if (confirm('Are you sure you want to remove this person?')) {
            this.manager.removePerson(personId);
        }
    }
    toggleItemForPerson(personId, itemId) {
        this.manager.toggleItemForPerson(personId, itemId);
    }
}
// Initialize when DOM is ready
let modernUI;
document.addEventListener('DOMContentLoaded', () => {
    modernUI = new ModernUI();
    // Make it globally available for onclick handlers
    window.modernUI = modernUI;
});
