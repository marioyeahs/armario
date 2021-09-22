function setInputFilter(textbox, inputFilter) {
[
    "input","keydown","keyup","mousedown","mouseup","select","contextmenu","drop",
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
    const mins = document.getElementsByClassName("min")
    const maxs = document.getElementsByClassName("max")
    for (var i=0;i < mins.length; i++){
        if(mins.item(i).innerHTML=="None") {
            mins.item(i).innerHTML = " Sold out! "
        }
    }
    for (var i=0;i < maxs.length; i++){
        if(maxs.item(i).innerHTML=="None") {
            maxs.item(i).innerHTML = " Sold out! "
        }
    }

    
    const submit_oferta_compra = document.getElementById('oferta_compra');
    const submit_oferta_venta = document.getElementById('oferta_venta');
    const monto = document.getElementById('intTextBox')
    const boton_compra = document.getElementsByClassName('comprar_ahora')
    const boton_venta = document.getElementsByClassName('vender_ahora')
    const radios = document.querySelectorAll("input[type=radio]");
    const submits = document.querySelectorAll("button");
    const check = document.getElementById("oferta");
    const tallas = document.getElementsByClassName("tallas")
    
    let indice=0;
    tallas[indice].checked = true;

    monto.value='';

    submit_oferta_venta.disabled=true;
    submit_oferta_compra.disabled=true;

    for(let i = 0;i<boton_compra.length;i++){
        boton_compra[i].disabled=true;
        boton_venta[i].disabled=true;
    }

    radios.forEach(function(radio){
        radio.onclick = function() {
            check.innerHTML=''
            monto.select()
            monto.value='';
            for (let i=0; i<tallas.length; i++){
                    if(tallas[i].checked == true){
                        if(i<=4){
                            let indice_compra = i;
                            localStorage.setItem('indice_compra',indice_compra)
                            if(localStorage.getItem('indice_venta')){
                                localStorage.removeItem('indice_venta')
                            }
                        }else{
                            let indice_venta = i-5;
                            localStorage.setItem('indice_venta',indice_venta)
                            if(localStorage.getItem('indice_compra')){
                                localStorage.removeItem('indice_compra')
                            }
                        }
                    }
            }
            for(let i = 0;i<boton_compra.length;i++){
                boton_compra[i].disabled=true;
                boton_venta[i].disabled=true;
            }
            let index = Array.prototype.indexOf.call(radios,radio);
            if(submits[index].value === 'None'){
                submits[index].disabled = true;
            }else{
                submits[index].disabled = false;
                
            }
        }
    });
    
    monto.onkeyup = (e) => {
        if (monto.value.length > 0){
            for(let i = 0;i<boton_compra.length;i++){
                boton_compra[i].disabled=true;
                boton_venta[i].disabled=true;
            }
            submit_oferta_venta.disabled=false;
            submit_oferta_compra.disabled=false;
        }else{
            submit_oferta_venta.disabled=true;
            submit_oferta_compra.disabled=true;
        }
        
        let offer = e.target.value; // la cantidad que se está escribiendo
        if(localStorage.getItem('indice_compra')){
            console.log("Oferta de compra")
            let highest_offer = mins[localStorage.getItem('indice_compra')].innerHTML;
            if(highest_offer=="None" || parseInt(highest_offer)<offer){
                check.innerHTML = "Tu puja será la más alta";
            }else if(parseInt(highest_offer)>offer){
                check.innerHTML = "Tu puja no es la más alta";
            }
        }else{
            console.log("Oferta de venta")
            let lowest_offer =maxs[localStorage.getItem('indice_venta')].innerHTML;
            if(lowest_offer=="None" || parseInt(lowest_offer)>offer){
                check.innerHTML = "Tu oferta será la más baja";
            }else if(parseInt(lowest_offer)<offer){
                check.innerHTML = "Tu oferta no es la más baja";
            }
        }
    }

    // Install input filters.
    setInputFilter(monto, function (value) {
        return /^\d*$/.test(value);
    });

});


