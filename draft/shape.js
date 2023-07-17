let currentTool = '';
let shapes = [];

function selectTool(tool) {
    currentTool = tool;
}

function startDrawing(event) {
    if (currentTool !== '' && event.buttons === 1) {
        promptForShapeName(event);
    }
}

function promptForShapeName(event) {
    let name = prompt(`Enter the name for the ${currentTool}:`);
    if (name === null) {
        return;
    }
    addShape(name, event);
}

function addShape(name, event) {
    let shapeContainer = document.createElement("div");
    shapeContainer.style.position = "absolute";
    shapeContainer.style.left = event.clientX + "px";
    shapeContainer.style.top = event.clientY + "px";

    let shape = document.createElement("object");
    shape.className = "shape";
    shape.type = "image/svg+xml";
    shape.data = currentTool + ".svg";
    shape.style.position = "relative";
    shape.onload = function () {
        let svgDocument = shape.contentDocument;
        let shapeName = svgDocument.getElementById("text-id");
        shapeName.textContent = name;
    };

    shape.addEventListener("contextmenu", function (e) {
        e.preventDefault();

        let contextMenu = document.createElement("div");
        contextMenu.className = "context-menu";
        contextMenu.style.position = "absolute";
        contextMenu.style.left = e.clientX + "px";
        contextMenu.style.top = e.clientY + "px";

        let moveOption = document.createElement("div");
        moveOption.textContent = "Move";
        moveOption.addEventListener("click", function () {

        });

        let deleteOption = document.createElement("div");
        deleteOption.textContent = "Delete";
        deleteOption.addEventListener("click", function () {

        });

        contextMenu.appendChild(moveOption);
        contextMenu.appendChild(deleteOption);

        // document.body.appendChild(contextMenu);
        document.getElementById("whiteboard").appendChild(contextMenu);
    })

    document.getElementById("whiteboard").appendChild(shapeContainer);
    shapeContainer.appendChild(shape);

    shapes.push({ type: currentTool, name: name });
}

function moveShape(shapeContainer) {
    let startX, startY;

    function onMouseMove(e) {
        let deltaX = e.clientX - startX;
        let deltaY = e.clientY - startY;
        shapeContainer.style.left = parseInt(shapeContainer.style.left) + deltaX + "px";
        shapeContainer.style.top = parseInt(shapeContainer.style.top) + deltaY + "px";
        startX = e.clientX;
        startY = e.clientY;
    }

    function onMouseUp() {
        document.removeEventListener("mousemove", onMouseMove);
        document.removeEventListener("mouseup", onMouseUp);
    }

    shapeContainer.addEventListener("mousedown", function (e) {
        startX = e.clientX;
        startY = e.clientY;
        document.addEventListener("mousemove", onMouseMove);
        document.addEventListener("mouseup", onMouseUp);
    });
}

function deleteShape(shapeContainer) {
    shapeContainer.remove();
    shapes = shapes.filter(function (shape) {
        return shapeContainer.querySelector(".shape").data !== shape.type + ".svg";
    });
}


function displayShapes() {
    console.log("Saved Shapes:");
    for (let i = 0; i < shapes.length; i++) {
        console.log("Type: " + shapes[i].type + ", Name: " + shapes[i].name);
    }
}