function toggle_comment(pk) {
    var box = document.getElementById(pk)
    if ( box.style.display === 'none' ){ 
        box.style.display = 'block'; 
    } else {
         box.style.display = 'none'; 
    }
}

function formSubmit() {
    var main_category = document.getElementById('main_category');
    var main_selected = main_category.options[main_category.selectedIndex].innerText;
    var title = document.getElementById('title');
    var content = document.querySelector('textarea.ace_text-input');
    if (main_selected === '-') {
        alert("메인 카테고리를 선택 해 주세요.");
        return false;
    } else if (title.innerText === "") {
        alert("제목을 입력 해 주세요.");
        return false;
    } else if (content.innerText === "") {
        alert("내용을 입력 해 주세요.");
        return false;
    }
}

function form_answer() {
    var title = document.getElementById('title');
    var content = document.querySelector('textarea.ace_text-input');
    if (title.innerText === "") {
        alert("제목을 입력 해 주세요.");
        return false;
    } else if (content.innerText === "") {
        alert("내용을 입력 해 주세요.");
        return false;
    }
}

function remove_self(e) {
    e.target.parentNode.parentNode.removeChild(e.target.parentNode);
}

function enterkey() {
    if (window.event.keyCode != 13) {
        return;
    }
    var tag_list = document.getElementById('tag_list');
    var tag_list_dom = document.querySelectorAll('#tag_list > span');
    var tag_input = document.getElementById('tag_input');

    if (tag_input.value === "") {
        alert("태그를 입력해주세요.");
        return;
    }

    for (var i = 0; i < tag_list_dom.length; i++) {
        if (tag_list_dom[i].innerText === tag_input.value) {
            alert("이미 태그가 존재합니다.");
            return;
        }
    }

    var tag = document.createElement('span');
    tag.setAttribute("class", "tag");
    
    var hidden = document.createElement('input');
    hidden.setAttribute("type", "hidden");
    hidden.setAttribute("name", "tag[]");
    hidden.setAttribute("value", tag_input.value);

    var circle = document.createElement('i');
    circle.setAttribute("class", "fas fa-times-circle");
    circle.addEventListener('click', remove_self, false);
    
    tag.innerText = tag_input.value;
    tag.append(circle);
    tag.append(hidden);
    
    tag_list.append(tag);
    tag_input.value = "";
}