var ques = []
var n = 0

$("#add-q").click(e => {
    e.preventDefault();
    let new_q = $("#q").val().trim();
    if(new_q === "") return
    ques.push(new_q);
    n += 1;
    $("#qss").append(`
        <div id="q-${n}" class="row justify-content-center mb-1">
            <div class="col-lg-5 col-8 border me-2 questions">${new_q}</div>
            <button class="col-lg-2 col-3 btn btn-danger" type="button" id="del-q-${n}" class="del-q" onclick="handleDelQ('q-${n}')">Remove</button>
        </div>        
    `);
    $("#q").val("");
})

const handleDelQ = id => {
    let q = $(`#${id}`).children("div").text();
    $(`#${id}`).remove();
    ques = ques.filter(x => x !== q);
}

$("#f-ask").submit(e => {
    e.preventDefault();
    fetch("/ask", {
        method: "POST",
        body: JSON.stringify({
            "questions": ques,
            "issueId": issueId, 
        }),
        headers: {
            "Content-type": "application/JSON; charset=UTF-8"
        }
    }).then(
        response => response.json()
    ).then(
        json => {
            if(json.message === "success"){
                location.href = "/"
            }
            else{
                window.alert("Something went wrong.")
            }
        }
    )
})