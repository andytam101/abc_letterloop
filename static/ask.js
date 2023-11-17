var ques = []
var n = 0

$("#add-q").click(e => {
    e.preventDefault();
    let new_q = $("#q").val();
    ques.push(new_q);
    n += 1;
    $("#qss").append(`
        <div id="q-${n}">
            <div>${new_q}</div>
            <button type="button" id="del-q-${n}" class="del-q" onclick="handleDelQ('q-${n}')">X</button>
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
            "issueID": issueID,
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