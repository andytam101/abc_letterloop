$(document).ready(() => {
    fetch("/get-latest-issue", {
        method: "GET"
    }).then(
        response => response.json()
    ).then(
        json => {
            if (json.status === "success") {
                json.questions.forEach(q => {
                    const html = addQuestionToContent(q)
                    $("#issue-content-div").append(html)
                })
            }
        }
    )
})


const addQuestionToContent = question => {
    const start = `<div class="row border rounded-3 bg-light mb-3 pt-2 pb-2">`
    const questionHtml = `
        <div class="pb-2 mb-2 col-12 col-lg-12 fst-italic fs-5 me-1 border-bottom">
            <b>${question.name} asked:</b> ${question.content}
        </div>
        `
    const ansStart = "<div>"

    let answers = ""
    question.answers.forEach(answer => {
        answers += `<div><b style="color:darkslateblue">${answer.name}</b>: ${answer.content}</div>`
    })
    const end = "</div></div>"

    return start + questionHtml + ansStart + answers + end
}
