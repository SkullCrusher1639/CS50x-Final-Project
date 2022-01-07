document.addEventListener("DOMContentLoaded",function(){
    // For the categories
    type_selector = document.querySelector("#type_selector")
    category_selector = document.querySelector("#category_selector")
    type_selector.addEventListener("change", function(){
        $.get("/type?q=" + type_selector.value, function(categories){
            let html = "<option value = '' selected disabled>Category</option>"
            for (let id in categories) {
                html += "<option value=" + categories[id].id + ">" + categories[id].category + "</option>"
            }
            document.querySelector("#category_selector").innerHTML = html
            document.querySelector("#sub_category_selector").innerHTML = "<option value = '' selected disabled>Sub-Category</option>"
        })
    })

    category_selector.addEventListener("change", function(){
        $.get("/cat?q=" + category_selector.value, function(sub_categories){
            let html = "<option value = '' selected disabled>Sub-Category</option>"
            for (let id in sub_categories) {
                html += "<option value=" + sub_categories[id].id + ">" + sub_categories[id].sub_category + "</option>"
            }
            document.querySelector("#sub_category_selector").innerHTML = html
        })
    })
})