$(document).ready(() => {
    $("#select-table").change(e => {
        const tableName = e.currentTarget.value
        loadTable(tableName)
    })

    loadTable("User")
})


const loadTable = tableName => {
    $("#table tbody").html("")
    const params = new URLSearchParams({
        tableName: tableName
    })

    fetch("/admin-info?" + params.toString())
        .then( response => response.json())
        .then( json => {
            if (json.status === "success") {
                displayTable(json.result)
            } else {
                alert(`Error: ${json.message}`)
            }
        })
}


const displayTable = table => {
    // assume table has one or more entry
    const row0 = table[0]
    const fields = Object.keys(row0)

    const headerRow = buildHeaderRow(fields)
    $("#header-row").html(headerRow)

    table.forEach(row => {
        const rowContent = Object.values(row)
        const rowHTML = buildContentRow(rowContent)
        $("#table tbody").append(rowHTML)
    })
}


const buildHeaderRow = fields => {
    let result = ""
    const cellStart = "<th>"
    const cellEnd = "</th>"
    fields.forEach( field =>
        result += (cellStart + field + cellEnd)
    )
    return result
}

const buildContentRow = contents => {
    let result = ""
    const cellStart = "<td>"
    const cellEnd = "</td>"
    contents.forEach( value =>
        result += (cellStart + value + cellEnd)
    )
    return `<tr>${result}</tr>`
}
