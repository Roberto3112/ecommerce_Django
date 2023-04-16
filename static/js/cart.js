console.log(`User: ${user}`)
let btns = document.getElementsByClassName('update-cart')

for(let i = 0; i < btns.length; i++){
    btns[i].addEventListener('click',() => {
        // shipping to access our data atributes that we already define in store.html
        let productID = btns[i].dataset.product
        let action = btns[i].dataset.action
        console.log(`ID: ${productID}, product: ${action}`)

        if(user == 'AnonymousUser'){
            console.log('Not logged in')
        }
        else{
            updateOrderItem(productID,action)
        }
    })
}

//! Note: Everytime we wanna send data to backend with Django we need the CRSFtoken. Go to main.html.
const updateOrderItem = (productID,action) =>{

    console.log('User is logged in, sending data...')

    // shipping to send the data to backend.

    // we have to specificate where we wanna send the data.
    let url = '/update_item/'

    //To send the data we have to use fetch
    //We past the URL and we have to specificate what kind of data we wanna send to

    fetch(url, {
        //* 1 - We're passing the data
        method: 'POST',
        // shipping an object.
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        //The body is what we wanna send to the url.
        //we use json.string to send shipping object as string.
        body:JSON.stringify({'productID':productID, 'action':action})
    })

    //*2 - We're getting the response in JSON value.
    // we have to return a promise that will be the response that we get, after we send that data to the view
    // we'll return: Item was added.
    .then((response) =>{
        return response.json()
    })

    //Here we'll console out the data we get that is the inicial string that have our view.
    //*3 - We're console out.
    .then((data) =>{
        console.log('data:',data)
        location.reload()
    })
}