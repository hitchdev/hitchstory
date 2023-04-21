const todoList = document.getElementById('todoList');
const addItemForm = document.getElementById('addItemForm');
const itemInput = document.getElementById('itemInput');
const addItemError = document.getElementById('addItemError');
const removeItemForm = document.getElementById('removeItemForm');
const indexInput = document.getElementById('indexInput');
const removeItemError = document.getElementById('removeItemError');

function displayTodoList() {
  fetch('/todo')
    .then(response => response.json())
    .then(data => {
      todoList.innerHTML = '';
      data.forEach((item, index) => {
        const li = document.createElement('li');
        li.classList.add('test-todo-list-item');
        li.textContent = item;
        const removeButton = document.createElement('button');
        removeButton.textContent = 'Remove';
        removeButton.addEventListener('click', () => removeItem(index + 1));
        li.appendChild(removeButton);
        todoList.appendChild(li);
      });
    });
}

function addItem(item) {
fetch('/todo', {
    method: 'POST',
    headers: {
    'Content-Type': 'application/json'
    },
    body: JSON.stringify({ item })
})
    .then(response => {
    if (response.ok) {
        displayTodoList();
    } else if (response.status === 400) {
        response.json().then(data => {
        const correctionMessage = `Did you mean "${data.message}"?`;
        addItemError.innerHTML = `${correctionMessage} <a href="#">(click to use)</a>`;
        addItemError.querySelector('a').addEventListener('click', () => {
            itemInput.value = data.message;
            addItemError.textContent = '';
        });
        setTimeout(() => {
            addItemError.textContent = '';
        }, 20000);
        });
    } else {
        addItemError.textContent = 'Failed to add item: ' + response.statusText;
        setTimeout(() => {
        addItemError.textContent = '';
        }, 20000);
    }
    });
}
  

function removeItem(item) {
  fetch(`/todo/${item}`, {
    method: 'DELETE'
  })
    .then(response => {
      if (response.ok) {
        displayTodoList();
      } else {
        removeItemError.textContent = 'Failed to remove item: ' + response.statusText;
      }
    });
}

displayTodoList();

addItemForm.addEventListener('submit', event => {
  event.preventDefault();
  const item = itemInput.value.trim();
  if (item === '') {
    addItemError.textContent = 'Please enter an item.';
    return;
  }
  addItem(item);
  itemInput.value = '';
});

removeItemForm.addEventListener('submit', event => {
  event.preventDefault();
  const index = parseInt(indexInput.value);
  if (isNaN(index) || index <= 0) {
    removeItemError.textContent = 'Please enter a valid index.';
    return;
  }
  removeItem(index);
  indexInput.value = '';
});
