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
    
    const submit_oferta_compra = document.getElementById('oferta_compra');
    const submit_oferta_venta = document.getElementById('oferta_venta');
    const monto = document.getElementById('intTextBox')
    const boton_compra = document.getElementsByClassName('comprar_ahora')
    const boton_venta = document.getElementsByClassName('vender_ahora')
    const radios = document.querySelectorAll("input[type=radio]");
    const submits = document.querySelectorAll("button");
    const check = document.getElementById("oferta");
    const tallas = document.getElementsByClassName("tallas")
    const mins = document.getElementsByClassName("min")
    const maxs = document.getElementsByClassName("max")
    let indice=0;
    tallas[indice].checked = true;


    monto.value='';

    document.querySelectorAll('span').forEach(function(price){
        document.body.onload = function(){
            if(price.innerHTML==="None"){
                price.innerHTML="Sold out!"
            }
        }
    });

    submit_oferta_venta.disabled=true;
    submit_oferta_compra.disabled=true;

    for(let i = 0;i<boton_compra.length;i++){
        boton_compra[i].disabled=true;
        boton_venta[i].disabled=true;
    }

    radios.forEach(function(radio){
        radio.onclick = function() {
            var cambio;
            check.innerHTML=''
            monto.value='';
            for (let i=0; i<tallas.length; i++){
                    if(tallas[i].checked == true){
                        indice = i;
                        console.log(indice);
                        console.log(tallas[indice].value);
                        cambio = false
                    }
                    if(indice>=5){
                        indice = indice-5;
                        console.log(indice)
                        cambio = true
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
        console.log(offer)

        try{
            if(cambio==false){
                let highest_offer = mins[indice].innerHTML;
                if(highest_offer=="None" || parseInt(highest_offer)<offer){
                    check.innerHTML = "Tu oferta será la más alta";
                }else if(parseInt(highest_offer)>offer){
                    check.innerHTML = "Tu oferta no es la más alta";
                }
            }

        }finally{
            indice = 5-indice;
            let lowest_offer =maxs[indice].innerHTML;
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

    // monto.onkeydown = function () {
    //     console.log("ok!")
    // }

    // monto.onkeyup = check;
    
    


});


