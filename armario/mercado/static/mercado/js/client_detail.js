function show(className){
    fetch(`./${className}`)
    .then(response => response.text())
    .then( text => {
        document.querySelectorAll('div').display = "none";
        div = document.getElementById(`${className}`)
        div.display = "block";
        div.innerHTML = text;

        // document.getElementById("offers").style.display="none";
        // document.getElementById("edit_profile").style.display="none";
        // document.getElementById("purchases").style.display="none";
        // document.getElementById("bids").style.display="block";
        // document.querySelector('#bids').innerHTML = text;
    });
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('button').forEach(button => {
        button.onclick = function() {
            // console.log(this.className);
            //show_my_bids();
            show(this.className);
            // if(this.className=="bids"){
            //     // alert("bids");
            //     show_my_bids();
            // }
        }
    });
})