but = document.getElementById('addtask');
selector = document.getElementsByClassName('choose-command')[0];
ul = document.getElementsByTagName('ul')[0]

forms = {
    '0': document.getElementById('site'),
    '1': document.getElementById('app'),
    '2': document.getElementById('thanks'),
    '3': document.getElementById('app'),
    '4': document.getElementById('internet'),
    '5': document.getElementById('yt')
}

function proc() {
    eel.start_process_commands()(function(res) {});
    eel.getJson('commands.json')(function(result) {
        for (i = 0; i < Object.keys(result).length; i++) {
            if (result[String(i)]['commands'] == 'browser') {
                const comand = `            
                <div class="list-item">
                    <p class="invisible">${i}</p>
                    <input class="text-area" onchange="changeWords(this)" placeholder="${result[String(i)]['url']}" type="text">
                    <p class="name-command">Open site</p>
                    <button class="minus-button" onclick="remove(this)">-</button>
                </div>`;
                ul.insertAdjacentHTML('beforeend', comand);
            } else if (result[String(i)]['commands'] == 'openapp') {
                const comand = `            
                <div class="list-item">
                    <p class="invisible">${i}</p>
                    <input class="text-area" onchange="changeWords(this)" placeholder="${result[String(i)]['path']}" type="text">
                    <p class="name-command">Open app</p>
                    <button class="minus-button" onclick="remove(this)">-</button>
                </div>`;
                ul.insertAdjacentHTML('beforeend', comand);
            }
            let words = result[String(i)]['words'];
            document.getElementsByClassName('text-area')[document.getElementsByClassName('text-area').length - 1].value = words.join(', ');
        }
    });
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

function changeName(el) {
    el.parentNode.getElementsByTagName('span')[0].innerHTML = el.files[0].name;
}

function changeForm(el) {
    val = Number(el.value);
    for (i = 0; i < 6; i++) {
        forms[i].style.display = 'none'
    }
    forms[val].style.display = 'block'
}

function addNewCommand() {
    a = selector.value;
    let url = document.getElementsByClassName('center-text-area')[0].value;
    d = {
        'comand': Number(a),
        'url': url,
        'path': forms['1'].getElementsByTagName('span')[0].innerHTML,
    }
    if (!url && a == '0' || forms['1'].getElementsByTagName('span')[0].innerHTML == 'Выберите файл' && (a == '1' || a == '3')) {
        return;
    }
    if (a == '0') {
        let elements = document.getElementsByClassName('text-area');
        for (let element of elements) {
            if (element.getAttribute('placeholder') == url) {
                console.log("URL already exists: ", url);
                return; // Exit if match found
            }
        }
    }
    // Add task asynchronously
    eel.add_task(d)(function(taskAdded) {
        if (taskAdded) {
            console.log("Task was successfully added");

            // Get the last task ID
            eel.lastID()(function(lastID, comN) {
                console.log("Last ID retrieved: ", lastID);
                eel.lastN()(function(c) {
                    console.log(c);
                    if (c == 0) {
                        const comand = `            
                            <div class="list-item">
                                <p class="invisible">${lastID}</p>
                                <input class="text-area" onchange="changeWords(this)" placeholder="${url}" type="text">
                                <p class="name-command">Open site</p>
                                <button class="minus-button" onclick="remove(this)">-</button>
                            </div>`;
                        ul.insertAdjacentHTML('beforeend', comand);
                    } else if (c == 1) {
                        const comand = `            
                            <div class="list-item">
                                <p class="invisible">${lastID}</p>
                                <input class="text-area" onchange="changeWords(this)" placeholder="${d['path']}" type="text">
                                <p class="name-command">Open app</p>
                                <button class="minus-button" onclick="remove(this)">-</button>
                            </div>`;
                        ul.insertAdjacentHTML('beforeend', comand);
                    }
                })
            });
        } else {
            console.error("Task was not added, taskAdded = ", taskAdded);
        }
    });
}



function remove(elem) {
    id = elem.parentNode.getElementsByClassName('invisible')[0].innerHTML;
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