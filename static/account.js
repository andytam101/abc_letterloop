$("#f-register").submit(e => {
    e.preventDefault();
    var formData = new FormData(e.target);

    if(formData.get("pw") !== formData.get("confirm-pw")){
        window.alert("The 2 passwords do not match!");
        console.log(formData.get("pw"));
        console.log(formData.get("confirm-pw"))
        return
    }

    fetch("/register", {
        method: "POST",
        body: formData,
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
        body: formData
    }).then(
        response => response.json()
    ).then(
        result => {
            if(result.message === "success"){
                sessionStorage.setItem("username", formData.get("name"))
                location.href = "/";
            }
            else if(result.message === "email"){
                window.alert("Email cannot be found.")
            }
            else if(result.message === "password"){
                window.alert("Incorrect password.")
            }
            else{
                window.alert("Failed to login. Something went wrong.");
            }
    })
})