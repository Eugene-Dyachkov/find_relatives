import sendRequest from './sendRequest.js';


const requestURL = 'http://127.0.0.1:8000/user/user/registration/'


// sendRequest('GET', requestURL)
//   .then(data => console.log(data))
//   .catch(err => console.log(err))

function validateEmail(inputText) {
  var mailFormat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
  if (inputText.value.match(mailFormat)) {
    return true;
  } else {
    return false;
  }
}

document.querySelector("#register").onclick = function(){
  const body = {
    username: document.querySelector('#username').value,
    email: document.querySelector('#email').value,
    password: document.querySelector('#password').value
  }
  if (validateEmail(email) == true) {
    sendRequest('POST', requestURL, body)
      .then(data => alert(data['detail']))
      .catch(err => alert(err['detail']))
  } else {
    alert("Invalid address!!!!");
  }
}
