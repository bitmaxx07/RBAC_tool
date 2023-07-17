let categoryList = []

function addCategory() {
    const categoryNameInput = document.getElementsById('category-name-input');
    const categoryName = categoryNameInput.value.trim();

    if (categoryName === '') {
        alert('Please enter a category name!');
        return;
    }

    const isDuplicate = categoryList.some(c => c.name === categoryName);
    if (isDuplicate) {
        alert('A category with the same name exists already');
        return;
    }

    const categoryListContainer = document.getElementById('category-list');

    const categoryId = `category-${categoryName}`;

    const categoryContainer = document.createElement('div');
    categoryContainer.classList.add('category-container');
    categoryContainer.setAttribute('data-id', categoryId);
    categoryContainer.setAttribute('node-name', categoryName);

    const category = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    category.setAttribute('id', categoryId);
    category.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    category.setAttribute('width', '100');
    category.setAttribute('height', '50');

    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', '10');
    text.setAttribute('y', '20');
    text.textContent = categoryName;

    category.appendChild(text);

    categoryContainer.appendChild(category);

    const optionsMenu = document.createElement('div');
    optionsMenu.classList.add('options-menu');

    const addChildOption = document.createElement('div');
    addChildOption.textContent = 'Add child';
    addChildOption.classList.add('option');

    const addUserOption = document.createElement('div');
    addUserOption.textContent = 'Add endpoint';
    addUserOption.classList.add('option');

    const deleteOption = document.createElement('div');
    deleteOption.textContent = 'Delete';
    deleteOption.classList.add('option');

    optionsMenu.appendChild(addChildOption);
    optionsMenu.appendChild(deleteOption);
    optionsMenu.appendChild(addUserOption);

    categoryContainer.appendChild(optionsMenu);

    // TODO: CONFIGURE HERE
    addChildOption.addEventListener('click', addChild);
    deleteOption.addEventListener('click', deleteCategory);
    addUserOption.addEventListener('click', addUser);

    categoryListContainer.appendChild(categoryContainer);

    categoryList.push({ id:categoryId, name: categoryName, type: 'image/svg+xml', content: categoryContainer.innerHTML });

}

function deleteCategory() {
    const categoryContainer = event.target.closest('.category-container');
    const categoryId = categoryContainer.getAttribute('data-id');
    const index = categoryList.findIndex(c => c.id === categoryId);
    if (index !== -1) {
        categoryList.splice(index, 1);
    }

    const deletedChildren = categoryList.filter(c => c.parentId === categoryId);
    deletedChildren.forEach(c => {
        c.container.remove();
        categoryList.splice(categoryList.indexOf(child), 1);
    });

    categoryContainer.remove();
    categoryList.splice(index, 1);

    // TODO: update XML here
}

function addChild(event) {
    const categoryContainer = event.target.closest('.category-container');
    const motherCategoryId = categoryContainer.getAttribute('data-id');
    const motherCategoryIndex = categoryList.findIndex(c => c.id === motherCategoryId);

    const categoryName = prompt('Enter child name:');
    if (categoryName === '') {
        alert('Please enter a category name!');
        return;
    }

    const isDuplicate = categoryList.some(c => c.name === categoryName);
    if (isDuplicate) {
        alert('A category with the same name exists already!');
        return;
    }

    if (motherCategoryIndex === -1) {
        alert('Mother category not found!');
        return;
    }

    const childCategoryId = `category-${categoryName}`;

    const childCategoryContainer = document.createElement('div');
    childCategoryContainer.classList.add('category-container');
    childCategoryContainer.setAttribute('data-id', childCategoryId);
    childCategoryContainer.setAttribute('node-name', categoryName);

    // const rowContainer = categoryContainer.closest('.row-container');

    const childCategory = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    childCategory.setAttribute('id', childCategoryId);
    childCategory.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    childCategory.setAttribute('width', '75');
    childCategory.setAttribute('height', '25');

    const childText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    childCategory.setAttribute('x', '10');
    childCategory.setAttribute('y', '20');
    childCategory.textContent = categoryName + ":" + categoryContainer.getAttribute('node-name');

    childCategory.appendChild(childText);
    childCategoryContainer.appendChild(childCategory);

    const optionsMenu = document.createElement('div');
    optionsMenu.classList.add('options-menu');

    const addChildOption = document.createElement('div');
    addChildOption.textContent = 'Add child';
    addChildOption.classList.add('option');

    const addUserOption = document.createElement('div');
    addUserOption.textContent = 'Add endpoint';
    addUserOption.classList.add('option');

    const deleteOption = document.createElement('div');
    deleteOption.textContent = 'Delete';
    deleteOption.classList.add('option');

    optionsMenu.appendChild(addChildOption);
    optionsMenu.appendChild(deleteOption);
    optionsMenu.appendChild(addUserOption);

    categoryContainer.appendChild(optionsMenu);

    const motherCategoryElement = document.getElementById(motherCategoryId);

    const rowContainer = categoryContainer.parentNode;

    const newRowContainer = document.createElement('div');
    newRowContainer.classList.add('row-container');
    newRowContainer.appendChild(motherCategoryElement.parentNode);

    const childRowContainer = document.createElement('div');
    childRowContainer.classList.add('row-container');
    childRowContainer.appendChild(childCategoryContainer);

    rowContainer.parentNode.insertBefore(newRowContainer, rowContainer.nextSibling);
    newRowContainer.parentNode.insertBefore(childRowContainer, newRowContainer.nextSibling);

    categoryList.push({ id: childCategoryId, name: 'Child Category', type: 'image/svg+xml', content: childCategoryContainer.innerHTML, parentId: motherCategoryId, container: childCategoryContainer});

    // TODO: update XML here
}

function addUser(event) {
    const categoryContainer = event.target.closest('.category-container');
    const motherCategoryId = categoryContainer.getAttribute('data-id');
    const motherCategoryIndex = categoryList.findIndex(c => c.id === motherCategoryId);

    const userName = prompt('Enter endpoint name:');
    if (userName === '') {
        alert('Please enter a category name!');
        return;
    }

    const isDuplicate = categoryList.some(c => c.name === userName);
    if (isDuplicate) {
        alert('An endpoint with the same name exists already!');
        return;
    }

    if (motherCategoryIndex === -1) {
        alert('Mother category not found!');
        return;
    }

    const userId = `endpoint-${userName}`;

    const userContainer = document.createElement('div');
    userContainer.classList.add('category-container');
    userContainer.setAttribute('data-id', userId);
    userContainer.setAttribute('node-name', userName);

    const user = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    user.setAttribute('id', userId);
    user.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    user.setAttribute('width', '75');
    user.setAttribute('height', '25');

    const userText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    userText.setAttribute('x', '10');
    userText.setAttribute('y', '20');
    userText.textContent = userName + ':' + userContainer.getAttribute('node-name');

    user.appendChild(userText);
    userContainer.appendChild(user);

    const optionsMenu = document.createElement('div');
    optionsMenu.classList.add('options-menu');

    const deleteOption = document.createElement('div');
    deleteOption.textContent = 'Delete';
    deleteOption.classList.add('option');

    optionsMenu.appendChild(deleteOption);
    userContainer.appendChild(optionsMenu);

    deleteOption.addEventListener('click', deleteCategory);

    let motherRowContainer = userContainer.closest('.row-container');

    if (!motherRowContainer) {
        const newRowContainer = document.createElement('div');
        newRowContainer.classList.add('row-container');
        newRowContainer.appendChild(userContainer.parentNode);
        userContainer.parentNode.parentNode.insertBefore(newRowContainer, userContainer.parentNode.nextSibling);
        motherRowContainer = newRowContainer;
    }

    const childContainers = motherRowContainer.querySelectorAll('.svg-container');
    const childRowIndex = Array.from(childContainers).indexOf(userContainer) + 1;

    const userObj = {
        id: userId,
        name: 'User',
        type: 'image/svg+xml',
        content: userContainer.innerHTML,
        parentId: motherCategoryId,
        container: userContainer
    };
    categoryList.splice(motherCategoryIndex + 1, 0, userObj);

    const motherCategoryElement = document.getElementById(motherCategoryId);
    const motherCategoryRect = motherCategoryElement.getBoundingClientRect();
    const userElement = userContainer.querySelectorAll('svg');
    const userRect = userElement.getBoundingClientRect();

    const arrowMarkerId = `arrow-${userName}`;

    const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
    marker.setAttribute('id', arrowMarkerId);
    marker.setAttribute('markerWidth', '10');
    marker.setAttribute('markerHeight', '10');
    marker.setAttribute('refX', '10');
    marker.setAttribute('refY', '3');
    marker.setAttribute('orient', 'autp');

    const arrowPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    arrowPath.setAttribute('d', 'M0,0 L0,6 L9,3 z');
    arrowPath.setAttribute('fill', 'black');

    marker.appendChild(arrowPath);
    motherCategoryElement.appendChild(marker);

    const arrowLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    arrowLine.setAttribute('x1', motherCategoryRectRect.x + motherCategoryRect.width / 2);
    arrowLine.setAttribute('y1', motherCategoryRectRect.y + motherCategoryRectRect.height);
    arrowLine.setAttribute('x2', userRect.x + userRect.width / 2);
    arrowLine.setAttribute('y2', userRect.y);
    arrowLine.setAttribute('stroke', 'black');

    motherCategoryElement.appendChild(arrowLine);

    // TODO: update XML here
}