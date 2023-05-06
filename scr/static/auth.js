import sendRequest from './sendRequest.js';


function validateEmail(inputText) {
  var mailFormat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
  if (inputText.match(mailFormat)) {
    return true;
  } else {
    return false;
  }
}

document.querySelector("#login").onclick = function(){
  email = document.querySelector('#email').value,
  password = document.querySelector('#password').value
  const requestURL = `http://127.0.0.1:8000/auth/token/${email}/${password}`
  if (validateEmail(email) == true) {
    sendRequest('GET', requestURL)
        .then(data => {
            localStorage.setItem("token",data['access_token']);
        })
        .catch(err => console.log(err))
  } else {
    alert("Invalid address!!!!");
  }
}
