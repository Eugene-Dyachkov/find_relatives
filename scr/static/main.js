window.addEventListener("DOMContentLoaded", () => {

    function relatives() {
        const request = new XMLHttpRequest();
        request.open("GET", "http://127.0.0.1:8000/user/user/my_relatives");
        request.setRequestHeader("Content-Type", "application/json");
        request.setRequestHeader('Authorization', "Bearer " + localStorage.token);
        request.send();
        request.addEventListener("load", function() {
            if (request.status == 200) {
                let data = JSON.parse(request.response);
                let add = document.createElement('div');

                add.classList.add('card');

                add.innerHTML = `
                    <a class="name" href="http://127.0.0.1:8000/pages/new_relative">Add a relative</a>
                `;
                document.querySelector('.app').appendChild(add)

                data.forEach(item => {
                    let card = document.createElement('div');

                    card.classList.add('card');

                    card.innerHTML = `
                        <div class="name">${item.last_name}</div>
                        <div class="name">${item.first_name}</div>
                        <div class="name">${item.surname}</div>
                        <div class="name">${item.sity}</div>
                        <div class="name">${item.birth_data}</div>
                        <div class="name">${item.death_data}</div>
                    `;
                    document.querySelector('.app').appendChild(card)

                })
            } else {
                window.alert("sometext");
            }
        })
    }
    relatives()
});


document.querySelector("#new_relative").onclick = function(){

    window.location.href = 'http://127.0.0.1:8000/pages/new_relative';

  }
