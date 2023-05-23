
const requestURL = 'http://127.0.0.1:8000/relatives/create'



document.querySelector("#add").onclick = function(){
    const body = {
        last_name: document.querySelector('#last_name').value,
        first_name: document.querySelector('#first_name').value,
        surname: document.querySelector('#surname').value,
        sity: document.querySelector('#sity').value,
        birth_data: document.querySelector('#birth_data').value,
        death_data: document.querySelector('#death_data').value
    }
    alert(sendRequest("POST", requestURL, body))
  }

function sendRequest(method, url, body = null) {
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': "Bearer " + localStorage.token
  }
    return fetch(url, {
      method: method,
      body: JSON.stringify(body),
      headers: headers
    }).then(response => {
      if (response.ok) {
        return response.json()
      }

      return response.json().then(error => {
        const e = new Error('Что-то пошло не так')
        e.data = error
        throw e
      })
    })
}

document.querySelector("#exit").onclick = function(){

  window.location.href = 'http://127.0.0.1:8000/pages/home';

}
