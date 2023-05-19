const api = "http://127.0.0.1:5000";

window.onload = () => {
    // BEGIN CODE HERE
    let searchButton = document.getElementById("searchSubmit");
    searchButton.onclick = searchButtonOnClick;

    let saveButton = document.getElementById("saveButton");
    saveButton.onclick = productFormOnSubmit;
    // END CODE HERE
}

searchButtonOnClick = () => {
    // BEGIN CODE HERE
    const searchValue = document.getElementById('searchBarInput').value;

    const res = new XMLHttpRequest();
    res.open("GET", `${api}/search?name=${searchValue}`);
    res.onreadystatechange = () => {
        if (res.readyState === 4) {
            if (res.status === 200) {
                // console.log(res.responseText);
                const resultTableBody = document.getElementById("tableBody");
                resultTableBody.innerHTML = "";

                const JSONResponse = JSON.parse(res.response);
                JSONResponse.forEach((array_element) => {
                        const tr = document.createElement('tr');
                        tr.innerHTML = `<tr>
                    <td>${array_element.id ?? ""}</td>
                    <td>${array_element.name ?? ""}</td>
                    <td>${array_element.production_year ?? ""}</td>
                    <td>${array_element.price ?? ""}</td>
                    <td>${array_element.color ?? ""}</td>
                    <td>${array_element.size ?? ""}</td>
                  </tr>`;
                        resultTableBody.appendChild(tr);

                    }
                )
            }
        }
    };
    res.send();

    // END CODE HERE
}

productFormOnSubmit = (event) => {
    // BEGIN CODE HERE
    event.preventDefault();
    const form = document.getElementById('inputForm');
    if (form.checkValidity()) {

        const formData = {};
        const formElements = form.querySelectorAll('input');

        formElements.forEach(element => {
            const {name, value, type} = element;
            let convertedValue;

            if (type === 'number') {
                convertedValue = parseInt(value);
            } else {
                convertedValue = value;
            }

            formData[name] = convertedValue;
        });

        const jsonData = JSON.stringify(formData);

        const res = new XMLHttpRequest();
        res.open("POST", `${api}/add-product`);
        res.onreadystatechange = () => {
            if (res.readyState === 4) {
                if (res.status === 200) {
                    alert("OK");
                    form.reset();
                }
            }
        };
        res.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        res.send(jsonData);


        //console.log(jsonData);
    } else {
        form.reportValidity();
    }

    // END CODE HERE
}
