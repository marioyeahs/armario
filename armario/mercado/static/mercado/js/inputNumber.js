


function setInputFilter(textbox, inputFilter) {
[
    "input",
    "keydown",
    "keyup",
    "mousedown",
    "mouseup",
    "select",
    "contextmenu",
    "drop",
].forEach(function (event) {
    textbox.addEventListener(event, function () {
    if (inputFilter(this.value)) {
        this.oldValue = this.value;
        this.oldSelectionStart = this.selectionStart;
        this.oldSelectionEnd = this.selectionEnd;
    } else if (this.hasOwnProperty("oldValue")) {
        this.value = this.oldValue;
        this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
    } else {
        this.value = "";
    }
    });
});
}

document.addEventListener("DOMContentLoaded", function(){
    // Install input filters.
    setInputFilter(document.getElementById("intTextBox"), function (value) {
        return /^\d*$/.test(value);
    });
});


