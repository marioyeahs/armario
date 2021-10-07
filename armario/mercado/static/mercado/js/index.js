function show_products_by_department(depto){
    fetch(`./departamento/${depto}`)
    .then(response => response.text())
    .then( text => {
        document.querySelector('#products_by_department').innerHTML = text;
    });
}

function show__products_by_brand(marca) {
    fetch(`./productos/${marca}/`)
    .then(response => response.text())
    .then(text => {
        document.querySelector('#products_by_brand').innerHTML = text;
    });
}

document.addEventListener('DOMContentLoaded', function(){

    document.querySelectorAll('button').forEach(button => {
        button.onclick = function() {
            document.getElementById('productos').style.display = 'none';
            show_products_by_department(this.dataset.depto);
            //show_products_by_brand(this.dataset.marca);
        }
    });
});