function update_store(store_id, product_id, qty, product){
    data = {
        "store_id" : store_id,
        "product_id" : product_id,
        "total_available" : product.total_available - qty,
        "total_sold" : product.total_sold
    }

    $.post(`http://127.0.0.1:8000/api/update`, data, function(result){
        console.log(result)
    })
}


$(document).ready(function(){
    $(document).on('click', '.button-act', function(){
        id = $(this).attr('id')
        $('.button-act').removeClass('active-toggle')
        $('.action-form').removeClass('shown')
        $(this).addClass('active-toggle')

        if(id == "buy-toggle"){
            $(".buy-form").addClass('shown')
        }else if(id == "move-toggle"){
            $(".move-form").addClass('shown')
        }else if(id == "replenish-toggle"){
            $(".replenish-form").addClass('shown')
        }
    })

    $(document).on('click', '#action-move', function(e){
        e.preventDefault()

        store_from = $(".move-list-from").val()
        store_to = $(".move-list-to").val()
        product_id = $(".move-product-list").val()
        qty = $(".move-quantity").val()
        
        $.get(`http://127.0.0.1:8000/api/detail/${store_from}/${product_id}`, function(result){
            console.log(result)
            if(result[0].total_available < qty){
                alert("You do not have enough product in that store. Try moving from central store or any other store")
            }else{
                update_store(store_from, product_id, qty, result[0])
            }
        })

    })
})