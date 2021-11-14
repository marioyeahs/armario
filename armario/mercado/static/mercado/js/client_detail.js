function show_my_bids(){
    fetch(`./pujas`)
    .then(response => response.text())
    .then( text => {
        document.getElementById("offers").style.display="none";
        document.getElementById("edit_profile").style.display="none";
        document.getElementById("purchases").style.display="none";
        document.getElementById("bids").style.display="block";
        document.querySelector('#bids').innerHTML = text;
    });
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('button').forEach(button => {
        button.onclick = () => {
            show_my_bids();
            // if(this.className=="bids"){
            //     // alert("bids");
            //     show_my_bids();
            // }
        }
    });
})