$("#f-register").submit(e => {
    e.preventDefault();
    var formData = new FormData(e.target);

    if(formData.get("pw") !== formData.get("confirm-pw")){
        window.alert("The 2 passwords do not match!");
        return
    }

    fetch("/register", {
        method: "POST",
        body: JSON.stringify(formData),
        headers: {
            "Content-type": "application/JSON; charset=UTF-8"
        }
    }).then(
        Response => Response.json()
    ).then(
        result => {
            if(result.message === "success"){
                location.href = "/login";
            }
            else{
                window.alert("Failed to make an account. Something went wrong.");
            }
    })
})

$("#f-login").submit(e => {
    e.preventDefault();
    var formData = new FormData(e.target);

    fetch("/login", {
        method: "POST",
        body: JSON.stringify(formData),
        headers: {
            "Content-type": "application/JSON; charset=UTF-8"
        }
    }).then(
        response => response.json()
    ).then(
        result => {
            if(result.message === "success"){
                sessionStorage.setItem("username", formData.get("name"))
                location.href = "/";
            }
            else if(result.message === "wrong name"){
                window.alert("Name cannot be found.")
            }
            else if(result.message === "wrong password"){
                window.alert("Incorrect password.")
            }
            else{
                window.alert("Failed to login. Something went wrong.");
            }
    })
})