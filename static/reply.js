$(() => {
    fetch("/get-latest-questions", {
        method: "GET"
    }).then(
        response => response.json()
    ).then(
        json => {
            if (json.status === "success") {
                json.questions.forEach(q => {
                    const html = addQuestion(q)
                    $("#f-reply").append(html)
                })
            }
        }
    )
})

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

const addQuestion = question => {
    const start = `<div class="form-group mb-3">`
    const label = `<label class="ms-1" for="q-${question.quesId}"><b>${question.username} asked:</b> ${question.content}</label>`
    const input = `<input placeholder="Write your reply" class="form-control mt-1" type="text" id="q-${question.quesId}" name="q-${question.quesId}">`
    const end = "</div>"
    return start + label + input + end
}