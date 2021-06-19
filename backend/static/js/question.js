function toggle_comment(pk) {
    var box = document.getElementById(pk)
    if ( box.style.display === 'none' ){ 
        box.style.display = 'block'; 
    } else {
         box.style.display = 'none'; 
    }
}