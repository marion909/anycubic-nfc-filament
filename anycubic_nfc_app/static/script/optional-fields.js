function toggleOptional(enabled) {
    if(enabled) {
        document.getElementById("optionalStyle").innerHTML = "";
    } else {
        document.getElementById("optionalStyle").innerHTML = ".optional {display: none;}";
    }
}

const changeCheckbox = document.getElementById('optionalFields')

changeCheckbox.addEventListener('change', (event) => {
  if (event.currentTarget.checked) {
    toggleOptional(true);
  } else {
    toggleOptional(false);
  }
})
