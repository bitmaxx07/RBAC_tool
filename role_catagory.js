let svgList = [];

// Function to show the SVG and add its ID and Name to the list
// Function to show the SVG and add its ID, Name, and Type to the list
function showSVG() {
    const svgNameInput = document.getElementById('svg-name-input');
    const svgName = svgNameInput.value.trim();

    // Check if SVG name is empty
    if (svgName === '') {
        alert('Please enter an SVG name.');
        return;
    }

    // Check for duplicate SVG names
    const isDuplicate = svgList.some(svg => svg.name === svgName);
    if (isDuplicate) {
        alert('An SVG with the same name already exists.');
        return;
    }

    const svgListContainer = document.getElementById('svg-list');

    // Create a unique ID for the SVG
    const svgId = `svg-${svgName}`;

    // Create a container div for the SVG and options
    const svgContainer = document.createElement('div');
    svgContainer.classList.add('svg-container');
    svgContainer.setAttribute('data-id', svgId);
    svgContainer.setAttribute('node-name', svgName);

    // Create the SVG element
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('id', svgId);
    svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    svg.setAttribute('width', '100');
    svg.setAttribute('height', '50');

    // Create a text element to display the SVG name
    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', '10');
    text.setAttribute('y', '20');
    text.textContent = svgName;

    // Append the text element to the SVG
    svg.appendChild(text);

    // Append the SVG to the container
    svgContainer.appendChild(svg);

    // Create the right-click options
    const optionsMenu = document.createElement('div');
    optionsMenu.classList.add('options-menu');

    const addChildOption = document.createElement('div');
    addChildOption.textContent = 'Add Child';
    addChildOption.classList.add('option');

    const deleteOption = document.createElement('div');
    deleteOption.textContent = 'Delete';
    deleteOption.classList.add('option');

    optionsMenu.appendChild(addChildOption);
    optionsMenu.appendChild(deleteOption);

    // Append the options menu to the container
    svgContainer.appendChild(optionsMenu);

    // Add event listeners to the options
    addChildOption.addEventListener('click', addChild);
    deleteOption.addEventListener('click', deleteSVG);

    // Append the container to the SVG list container
    svgListContainer.appendChild(svgContainer);

    const serializer = new XMLSerializer();
    const svgXML = serializer.serializeToString(svg);

    // Add the SVG object to the global list
    svgList.push({ id: svgId, name: svgName, type: 'image/svg+xml', content: svgContainer.innerHTML });
}

function addChild(event) {
    const svgContainer = event.target.closest('.svg-container');
    const motherSvgId = svgContainer.getAttribute('data-id');
    const motherSvgIndex = svgList.findIndex(svg => svg.id === motherSvgId);

    if (motherSvgIndex === -1) {
        alert('Mother SVG not found.');
        return;
    }

    const childName = prompt('Enter child name:');
    if (!childName) {
        return;
    }

    const duplicateChild = svgList.some(svg => svg.parentId === motherSvgId && svg.name === childName);
    if (duplicateChild) {
        alert('Child name already exists.');
        return;
    }

    const childSvgId = `svg-${childName}`;

    const childSvgContainer = document.createElement('div');
    childSvgContainer.classList.add('svg-container');
    childSvgContainer.setAttribute('data-id', childSvgId);
    childSvgContainer.setAttribute('node-name', childName);

    const childSvg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    childSvg.setAttribute('id', childSvgId);
    childSvg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    childSvg.setAttribute('width', '75');
    childSvg.setAttribute('height', '25');

    const childText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    childText.setAttribute('x', '10');
    childText.setAttribute('y', '20');
    childText.textContent = childName + ":" + svgContainer.getAttribute('node-name');

    childSvg.appendChild(childText);
    childSvgContainer.appendChild(childSvg);

    const optionsMenu = document.createElement('div');
    optionsMenu.classList.add('options-menu');

    const addChildOption = document.createElement('div');
    addChildOption.textContent = 'Add Child';
    addChildOption.classList.add('option');

    const deleteOption = document.createElement('div');
    deleteOption.textContent = 'Delete';
    deleteOption.classList.add('option');

    /*const deleteChildOption = document.createElement('div');
    deleteOption.textContent = 'Delete child';
    deleteChildOption.classList.add('option');*/

    optionsMenu.appendChild(addChildOption);
    optionsMenu.appendChild(deleteOption);
    childSvgContainer.appendChild(optionsMenu);

    addChildOption.addEventListener('click', addChild);
    deleteOption.addEventListener('click', deleteSVG);
    // deleteChildOption.addEventListener('click', deleteSVG);

    const motherSvgElement = document.getElementById(motherSvgId);
    const motherSvgRect = motherSvgElement.getBoundingClientRect();

    const rowContainer = svgContainer.parentNode;
    const motherContainerIndex = Array.from(rowContainer.children).indexOf(svgContainer);

    const newRowContainer = document.createElement('div');
    newRowContainer.classList.add('row-container');
    newRowContainer.appendChild(motherSvgElement.parentNode);

    rowContainer.parentNode.insertBefore(newRowContainer, rowContainer.nextSibling);

    const childRowContainer = document.createElement('div');
    childRowContainer.classList.add('row-container');
    childRowContainer.appendChild(childSvgContainer);

    newRowContainer.parentNode.insertBefore(childRowContainer, newRowContainer.nextSibling);

    svgList.push({ id: childSvgId, name: 'Child SVG', type: 'image/svg+xml', content: childSvgContainer.innerHTML, parentId: motherSvgId, container: childSvgContainer });

    // Update the XML
    updateXML();
}



function createSVGContainer(id, name, type, content) {
    const svgContainer = document.createElement('div');
    svgContainer.classList.add('svg-container');
    svgContainer.setAttribute('data-id', id);

    const svgElement = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svgElement.setAttribute('id', id);
    svgElement.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    svgElement.setAttribute('width', '75');
    svgElement.setAttribute('height', '25');

    svgContainer.appendChild(svgElement);

    const optionsMenu = document.createElement('div');
    optionsMenu.classList.add('options-menu');

    const addChildOption = document.createElement('div');
    addChildOption.textContent = 'Add Child';
    addChildOption.classList.add('option');

    const deleteOption = document.createElement('div');
    deleteOption.textContent = 'Delete';
    deleteOption.classList.add('option');

    optionsMenu.appendChild(addChildOption);
    optionsMenu.appendChild(deleteOption);
    svgContainer.appendChild(optionsMenu);

    addChildOption.addEventListener('click', addChild);
    deleteOption.addEventListener('click', deleteSVG);

    return svgContainer;
}


function deleteSVG() {
    const svgContainer = event.target.closest('.svg-container');
    const svgId = svgContainer.getAttribute('data-id');
    // svgContainer.parentNode.removeChild(svgContainer);
    const index = svgList.findIndex(svg => svg.id === svgId);
    if (index !== -1) {
        svgList.splice(index, 1);
    }

    const deletedChildren = svgList.filter(svg => svg.parentId === svgId);
    deletedChildren.forEach(child => {
        child.container.remove();
        svgList.splice(svgList.indexOf(child), 1);
    });

    svgContainer.remove();
    svgList.splice(index, 1);

    updateXML();
}

// Function to save the SVGs as a single XML file
function saveSVGs() {
    if (svgList.length === 0) {
        alert('No SVGs to save.');
        return;
    }

    const xmlData = [
        '<?xml version="1.0" standalone="no"?>',
        '<svgboard>'
    ];

    svgList.forEach(svg => {
        xmlData.push(`<svg id="${svg.id}" xmlns="http://www.w3.org/2000/svg" width="200" height="200">`);
        xmlData.push(svg.content);
        xmlData.push('</svg>');
    });

    xmlData.push('</svgboard>');

    const fullXmlData = xmlData.join('\n');

    const blob = new Blob([fullXmlData], { type: 'text/xml' });
    const url = URL.createObjectURL(blob);

    const downloadLink = document.createElement('a');
    downloadLink.href = url;
    downloadLink.download = 'svgboard.xml';
    downloadLink.click();

    URL.revokeObjectURL(url);

    // Clear the SVG list after saving
    svgList = [];
}

function updateXML() {
    const root = document.createElement('svg-list');

    // Helper function to find the parent SVG in the XML
    function findParentElement(parentId, elements) {
        for (const element of elements) {
            if (element.getAttribute('id') === parentId) {
                return element;
            }
            const childElements = element.getElementsByTagName('svg');
            const parentElement = findParentElement(parentId, childElements);
            if (parentElement) {
                return parentElement;
            }
        }
        return null;
    }

    // Iterate over the SVG list and create XML elements for each SVG
    svgList.forEach(svg => {
        if (!svg.parentId) {
            const svgElement = document.createElement('svg');
            svgElement.setAttribute('id', svg.id);
            svgElement.setAttribute('name', svg.name);
            svgElement.setAttribute('type', svg.type);
            svgElement.innerHTML = svg.content;
            root.appendChild(svgElement);
        } else {
            const parentElement = findParentElement(svg.parentId, root.children);
            if (parentElement) {
                const svgElement = document.createElement('svg');
                svgElement.setAttribute('id', svg.id);
                svgElement.setAttribute('name', svg.name);
                svgElement.setAttribute('type', svg.type);
                svgElement.innerHTML = svg.content;
                parentElement.appendChild(svgElement);
            }
        }
    });

    const serializer = new XMLSerializer();
    xmlContent = serializer.serializeToString(root);
}


// Attach event listener to the button
document.getElementById('show-button').addEventListener('click', showSVG);
document.getElementById('save-button').addEventListener('click', saveSVGs);
