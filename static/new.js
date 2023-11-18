$("#f-new").submit(e => {
    e.preventDefault();
    let formData = new FormData(e.target);

    // validate the dates

    // assume validated for now

    fetch("/new", {
        method: "POST",
        body: formData
    }).then(
        response => response.json()
    ).then(
        json => {
            console.log(json)
            if(json.message === "success"){
                location.href = "/"
            }
            else{
                console.log(json.message)
                window.alert("Something went wrong.")
            }
        }
    )
})