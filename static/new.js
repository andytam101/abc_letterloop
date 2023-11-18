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
            else if(json.message === "dates"){
                window.alert("Invalid dates. Deadline for answers must be after questions.")
            }
            else if(json.message === "ongoing"){
                window.alert("There is an ongoing issue. Go ask questions there!")
            }
            else{
                window.alert("Something went wrong.")
            }
        }
    )
})