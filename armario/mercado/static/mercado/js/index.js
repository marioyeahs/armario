function show_products(key){
    document.querySelectorAll('div').forEach(div => {
        div.style.display = 'none';
    });
    document.querySelector(`#${key}`).style.display = 'block';
}

function show_sections(marca) {
    fetch(`./productos/${marca}/`)
    .then(response => response.text()
    )
    .then(text => {
        document.querySelector('#content').innerHTML = text;
    });
}

document.addEventListener('DOMContentLoaded', function(){

    document.querySelectorAll('button').forEach(button => {
        button.onclick = function() {
            document.getElementById('productos').style.display = 'none';
            show_products(this.dataset.key);
            show_sections(this.dataset.marca);
        }
    });
});