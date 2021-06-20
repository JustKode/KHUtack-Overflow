function searchQuery() {
    var input = document.getElementById("query")
    if (input.value === "") {
        alert("검색어를 입력 해 주세요.")
        return
    }
    window.location.href = '/post/question/list/1?query=' + input.value
}