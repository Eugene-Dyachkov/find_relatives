const requestURL = 'http://127.0.0.1:8000/pages/hello'

// function sendRequest(method, url, body = null) {
//   const headers = {
//     'Content-Type': 'application/json'
//   }

//   return fetch(url, {
//     method: method,
//     body: JSON.stringify(body),
//     headers: headers
//   }).then(response => {
//     if (response.ok) {
//       return response.json()
//     }

//     return response.json().then(error => {
//       const e = new Error('Что-то пошло не так')
//       e.data = error
//       throw e
//     })
//   })
// }

// sendRequest('GET', requestURL)
//   .then(data => console.log(data))
//   .catch(err => console.log(err))

// const body = {
//     username: "string",
//     email: "userbbb@example.com",
//     password: "string"
// }

// sendRequest('POST', requestURL, body)
//   .then(data => console.log(data))
//   .catch(err => console.log(err))


// function sendRequest(method, url, body = null) {
//   const headers = {
//     'Content-Type': 'application/json'
//   }
// }



function register(method, url, body = null) {
  return(url).then(response => {
    return response.text()
  })
}

register('GET', requestURL)
  .then(data=>console.log(data))
  .catch(err=>console.log(err))


const body = {

}
