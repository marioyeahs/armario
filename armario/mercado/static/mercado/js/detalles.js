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
    
    const submit_oferta_compra = document.getElementById('oferta_compra');
    const submit_oferta_venta = document.getElementById('oferta_venta');
    const monto = document.getElementById('intTextBox')
    const boton_compra = document.getElementsByClassName('comprar_ahora')
    const boton_venta = document.getElementsByClassName('vender_ahora')
    const tallas = document.getElementsByClassName('tallas')
    const test = document.getElementById('check_test')

    for(let i = 0;i<boton_compra.length;i++){
        boton_compra[i].disabled=true;
        boton_venta[i].disabled=true;
    }
    
    submit_oferta_venta.disabled=true;
    submit_oferta_compra.disabled=true;

    document.querySelectorAll("input[type=radio]").forEach(function(radio){
        radio.change = function(){
            boton_compra[(radio.id)-1].disabled=false;
        }
    })
    
    monto.onkeyup = () => {
        if (monto.value.length > 0){
            submit_oferta_venta.disabled=false;
            submit_oferta_compra.disabled=false;
        }else{
            submit_oferta_venta.disabled=true;
            submit_oferta_compra.disabled=true;
        }
    }

    // Install input filters.
    setInputFilter(document.getElementById("intTextBox"), function (value) {
        return /^\d*$/.test(value);
    });
});


