// this for hide the shipping form if our product is digital

if(shipping == 'False' && user != 'AnonymousUser'){
    document.getElementById('button-div').classList.add('hidden')
    document.getElementById('payment-info').classList.remove('hidden')
    document.getElementById('shipping-info').innerHTML = ''
    document.getElementById('shipping-div').classList.remove('shipping-card')
    document.getElementById('shipping-div').classList.add('digital-card')
    }

// this is we click the continue button after we complete the form
// hide the button and the pay information show up.
let form = document.getElementById('form')
form.addEventListener('submit',(e) =>{
    e.preventDefault()
    console.log('form submited...')
    document.getElementById('button-div').classList.add('hidden')
    document.getElementById('payment-info').classList.remove('hidden')
})

let submitFormData = () => {
    console.log('Payment submitted.')
    // This is creating objects with null for default, and their values will be change.
    // We'll change the value getting all the values from the form.
    let userFormData = {
        'name':null,
        'email': null,
        'total': orderTotal,
    }

    let shippingInfo = {
        'address':null,
        'city': null,
        'state': null,
        'zipcode': null,
    }

    // get the form values and change the objects values.
    if(shipping != 'False'){
        shippingInfo.address = form.address.value
        shippingInfo.city = form.city.value
        shippingInfo.state = form.state.value
        shippingInfo.zipcode = form.zipcode.value
    }

    if(user == 'AnonymousUser'){
        userFormData.name = form.name.value
        userFormData.email = form.email.value   
    }

    url = '/process_order/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'shipping':shippingInfo, 'form':userFormData})
    })

    .then((response) =>{
        response.json()
    })

    .then((data) => {
        console.log('Data:', data)
        // To relocate the customer back to the homepage.
        alert('Transaction completed')
        window.location.href = storeUrl
    })      
}

document.getElementById('make-payment').addEventListener('click',()=>{
    submitFormData()
})

if(user != 'AnonymousUser'){
    document.getElementById('name-info').innerHTML = ''
} else{
    document.getElementById('shipping-info').classList.add('hidden')
    document.getElementById('shipping-div').classList.remove('shipping-card')
    document.getElementById('shipping-div').classList.add('digital-card')
}





