window.onload = function () {
	var objDiv = document.getElementById("chat_screen");
	objDiv.scrollTop = objDiv.scrollHeight;
}

var formSubmitted = false

window.addEventListener('beforeunload', function (e) {
    if (!formSubmitted) {
        e.preventDefault();
        e.returnValue = '';
    }
});