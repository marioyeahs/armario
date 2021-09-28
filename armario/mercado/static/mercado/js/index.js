function show_products(key){
    document.querySelectorAll('div').forEach(div => {
        div.style.display = 'none';
    });
    document.querySelector(`#${key}`).style.display = 'block';
}
