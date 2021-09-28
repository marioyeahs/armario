function show_products(key){
    document.querySelectorAll('div').forEach(div => {
        div.style.display = 'none';
    });
    document.querySelector(`#${key}`).style.display = 'block';
}

document.addEventListener('DOMContentLoaded', function(){

    document.querySelectorAll('button').forEach(button => {
        button.onclick = function() {
            document.getElementById('productos').style.display = 'none';
            show_products(this.dataset.key);
        }
    })
});