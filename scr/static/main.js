
function nameFunction() {
    const URL = 'http://127.0.0.1:8000/user/user/my_relatives'
    const token = localStorage.token;
    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    return fetch(URL, {
        method: 'GET',
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

const n = nameFunction()

console.log(n)
