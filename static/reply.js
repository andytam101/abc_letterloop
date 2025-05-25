$("#f-reply").submit(e => {
    e.preventDefault()
    var formData = new FormData(e.target)

    disableSubmit()

    fetch("/reply",{
        method: "POST",
        body: formData
    }).then(
        response => response.json()
    ).then(
        json => {
            if (json.message === "success") {
                location.href = "/"
            }
            else{
                console.log(json)
                window.alert("Failed. Something went wrong.")
                enableSubmit()
            }
        }
    )

})

const disableSubmit = () => {
    $("#submit-btn").text("Submitting...")
    $("#submit-btn").prop("disabled", true)
    $("#submit-btn").removeClass("btn-primary")
    $("#submit-btn").addClass("btn-secondary")
}

const enableSubmit = () => {
    $("#submit-btn").text("Submit")
    $("#submit-btn").prop("disabled", false)
    $("#submit-btn").removeClass("btn-secondary")
    $("#submit-btn").addClass("btn-primary")
}

