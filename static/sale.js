document.addEventListener("DOMContentLoaded",function(){
    let name_selector = document.querySelector("#name");
    name_selector.addEventListener("change", function(){
        $.get("/quantity?q=" + name_selector.value, function(quantity_required){
            console.log(name_selector.value)
            console.log(quantity_required.quantity);
            document.querySelector("#quantity").max = quantity_required.quantity;
        })
    })
})