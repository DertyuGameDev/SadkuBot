but = document.getElementById('addtask');
selector = document.getElementsByClassName('choose-command')[0];
ul = document.getElementsByTagName('ul')[0]

function proc() {
    eel.start_process_commands()(function(result) {});
}

function quit() {
    eel.quit()(function(result) {});
}

function changeWords(el) {
    let r = el.parentNode;
    eel.setCommandWords(el.value, r.getElementsByClassName("invisible")[0].innerHTML)(function(res) {
        console.log(el.value)
    });
}

function addNewCommand() {
    switch (selector.value) {
        case '0':
            let url = document.getElementsByClassName('center-text-area')[0].value;
            let elements = document.getElementsByClassName('text-area');

            // Check if the URL already exists
            for (let element of elements) {
                if (element.getAttribute('placeholder') == url) {
                    console.log("URL already exists: ", url);
                    return; // Exit if match found
                }
            }

            console.log("Proceeding to add task");

            // Add task asynchronously
            eel.add_task(0, url)(function(taskAdded) {
                console.log("Task add request completed");

                if (taskAdded) {
                    console.log("Task was successfully added");

                    // Get the last task ID
                    eel.lastID()(function(lastID) {
                        console.log("Last ID retrieved: ", lastID);

                        const comand = `            
                        <div class="list-item">
                            <p class="invisible">${lastID}</p>
                            <input class="text-area" onchange="changeWords(this)" placeholder="${url}" type="text">
                            <p class="name-command">Open site</p>
                            <button class="minus-button" onclick="remove(this)">-</button>
                        </div>`;

                        // Insert the new command into the list
                        ul.insertAdjacentHTML('beforeend', comand);
                        console.log("Command added to UI");
                    });
                } else {
                    console.error("Task was not added, taskAdded = ", taskAdded);
                }
            });

            console.log("Finished addNewCommand function");
    }
}



function remove(elem) {
    id = elem.parentNode.getElementsByClassName('invisible')[0];
    eel.removeByID(id);
    elem.parentNode.remove();
}

function changeChecker(el) {
    if (el.value) {
        but.disabled = false;
    } else {
        but.disabled = true;
    }
}

window.onload = function() {
    proc();
};
window.closed = function() {
    quit()
};