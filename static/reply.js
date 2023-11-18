$("#f-reply").submit(e => {
    e.preventDefault()
    var formData = new FormData(e.target)

    fetch("/reply",{
        method: "POST",
        body: formData
    }).then(
        response => response.json()
    ).then(
        json => {
            if(json.message === "success"){
                location.href = "/"
            }
            else{
                console.log(json)
                window.alert("Failed. Something went wrong.")
            }
        }
    )

})