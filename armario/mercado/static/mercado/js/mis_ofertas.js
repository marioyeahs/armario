
document.addEventListener("DOMContentLoaded", function() {
    
    document.querySelectorAll('button').forEach(function(button){
        button.onclick = function(){
            alert('Se ha borrado tu oferta con éxito!');
        }
    });

})