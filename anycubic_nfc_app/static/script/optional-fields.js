function updateOptional() {
    if(document.getElementById('optionalFields').checked) {
        document.getElementById("optionalStyle").innerHTML = "";
    } else {
        document.getElementById("optionalStyle").innerHTML = ".optional {display: none;}";
    }
}

updateOptional();

document.getElementById('optionalFields').addEventListener('change', (event) => {
    updateOptional();
})
