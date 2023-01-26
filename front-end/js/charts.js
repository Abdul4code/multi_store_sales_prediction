$(document).ready(function(){
    var context = $('#mycanvas')[0].getContext('2d')

    var data = {
        labels : ['21/01/995', '15/01/1998', '14/02/2004', '18/04/1947', '14/02/2004', '18/04/1947', '21/04/2002'],
        datasets : [{
            label : "Amount in Store",
            data : [40, 35, 60, 42, 25, 80, 50],
            borderWidth: 1,
            borderColor: 'blue',
            backgroundColor: 'blue',
        }, 
        {
            label : "Predicted in Sales",
            data : [40, 15, 24, 56, 62, 43, 20],
            borderWidth: 1,
            borderColor: 'brown',
            backgroundColor: 'brown',
        }]
    }

    var chart = new Chart(context, {
        type:'bar',
        data: data,
        option: {
        }
    })
})