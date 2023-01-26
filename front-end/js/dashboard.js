/*********************** populate the products dropdown ***********************************/ 
function fill_products_dropdown(unique_products){
    $('.product_list').empty()
    $('.product_list').append(`<option value='${0}'> All </>`)
    unique_products.forEach(element => {
        $('.product_list').append(`<option value='${unique_products.indexOf(element) + 1}'> ${element} </>`)
    });
}

/*********************** populate the stores dropdown ***********************************/ 
function fill_stores_dropdown(unique_stores){
    $('.stores_list').empty()
    $('.stores_list').append(`<option value='${0}'> All </>`)
    unique_stores.forEach(element => {
        $('.stores_list').append(`<option value='${unique_stores.indexOf(element) + 1}'> ${element} </>`)
    });
}

/*********************** populate the summary statistics ***********************************/ 
function fill_summary(all_stores, all_products, each_product_available){
     unique_stores = [...new Set(all_stores)]
     unique_products = [...new Set(all_products)]
     total_products = 0
     Object.values(each_product_available).forEach(val => {
         total_products = total_products + val
     })
     
     $("#unique_stores").text(unique_stores.length)
     $("#unique_products").text(unique_products.length)
     $("#total_items").text(total_products)
}


/*********************** Get products details ***********************************/ 
function get_details(products){
        all_stores = []
        all_products = []
        each_product_available = {}
        

        products.forEach(product => {
            store = product.store_name
            product_name = product.product_name

            each_product_available[product.product_id] = (
                each_product_available[product.product_id] ? 
                each_product_available[product.product_id] 
                += product.total_available : product.total_available
            )

            all_stores.push(store)
            all_products.push(product_name)
        })

        unique_stores = [...new Set(all_stores)]
        unique_products = [...new Set(all_products)]

        return  [
                all_stores, all_products,
                each_product_available, unique_stores, unique_products,
            ]
}

function default_method(){
    $.get("http://127.0.0.1:8000/api/products", function(result){
        details = get_details(result)
        all_stores = details[0]
        all_products = details[1]
        each_product_available = details[2]
        unique_stores = details[3]
        unique_products = details[4]

        fill_summary(all_stores, all_products, each_product_available)

        // populate the store selection options
        fill_stores_dropdown(unique_stores)
    
        // populate the products selection options
        fill_products_dropdown(unique_products)
       
    })
}

function change_store_or_product(){
    store_id = $(".stores_list").val()
    product_id = $(".product_list").val()

    $.get(`http://127.0.0.1:8000/api/filter/${store_id}/${product_id}`, function(result){
        console.log(result)
        details = get_details(result)
        all_stores = details[0]
        all_products = details[1]
        each_product_available = details[2]
        unique_stores = details[3]
        unique_products = details[4]

        fill_summary(all_stores, all_products, each_product_available)

        store_name = store_id == 0 ? "All Stores": result[0].store_name
        product_name = product_id == 0 ? "All Products" : result[0].product_name

        $('.sum-store').text(store_name)
        $('.sum-prod').text(product_name)
    })
}
    

$(document).ready(function(){
    // call default function 
    default_method()

    // on changing stores
    $(document).on('change', '.store_selection', function(){
        change_store_or_product()
    })
})