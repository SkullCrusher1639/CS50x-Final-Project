document.addEventListener("DOMContentLoaded",function(){
    let colors = ["blue", "green", "yellow", "orange", "pink", "red", "purple", "cyan", "gray", "indigo", "maroon", "khaki"]
    let months = []
    let sales = []
    let additions = []
    let net = []
    // Ajax call to get data form backend
    $.get("/months", function(monthly_data){
        document.querySelector("#report_chart").style.display = "none"
        for (let id in monthly_data){
            months.push(monthly_data[id].month)
            sales.push(monthly_data[id].sale)
            additions.push(monthly_data[id].add)
            net.push(monthly_data[id].net)
        }

        // Bar Chart Plotting
        new Chart("sale_chart", {
            type: "bar",
            data: {
            labels: months,
            datasets: [{
                label: "Sales",
                backgroundColor: colors,
                data: sales
            }]
            },
            options: {
                title: {
                display: true,
                text: "Monthly Sales"
                }
             }
        });

        new Chart("net_chart", {
            type: "bar",
            data: {
            labels: months,
            datasets: [{
                label: "Net Amount",
                backgroundColor: colors,
                data: net
            }]
            },
            options: {
               title: {
               display: true,
               text: "Net Sales"
               }
            }
        });

        new Chart("add_chart", {
            type: "bar",
            data: {
            labels: months,
            datasets: [{
                label: "Invenstments",
                backgroundColor: colors,
                data: additions
            }]
            },
            options: {
                title: {
                display: true,
                text: "Monthly Invenstments"
                },
                label: {display: false}
             }
        });
    })
    selection = document.querySelector("select")
    selection.addEventListener("change", function(){
        if (selection.value == "table"){
            document.querySelector("#report_table").style.display = "block"
            document.querySelector("#report_chart").style.display = "none"
        }
        else{
            document.querySelector("#report_table").style.display = "none"
            document.querySelector("#report_chart").style.display = "block"
        }
    })
})