function show_products_by_department(depto){
    fetch(`./departamento/${depto}`)
    .then(response => response.text())
    .then( text => {
        document.getElementById("products_by_brand").style.display="none";
        document.getElementById("products_by_department").style.display="block";
        document.querySelector('#products_by_department').innerHTML = text;
    });
}

function show_products_by_brand(marca) {
    fetch(`./productos/${marca}/`)
    .then(response => response.text())
    .then(text => {
        document.getElementById("products_by_department").style.display="none";
        document.getElementById("products_by_brand").style.display="block";
        document.querySelector('#products_by_brand').innerHTML = text;
    });
}

document.addEventListener('DOMContentLoaded', function(){

    document.querySelectorAll('button').forEach(button => {
        button.onclick = function() {
            if(this.className=="marca"){
                show_products_by_brand(this.dataset.marca);
            }else if(this.className=="depto"){
                show_products_by_department(this.dataset.depto);
            }
        }
    });
});