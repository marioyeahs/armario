function show(className){
    fetch(`./${className}s`)
    .then(response => response.text())
    .then( text => {
        document.querySelector('#bids').innerHTML = text;
    });
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('button').forEach(button => {
        button.onclick = function() {
            show(this.className);
        }
    });
})