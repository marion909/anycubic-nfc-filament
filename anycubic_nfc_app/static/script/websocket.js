const socket = io();

function updateConnectionState(connected) {
    if(connected) {
        document.getElementById("connectionDotStyle").innerHTML = "";
        document.getElementById("connectionState").innerHTML = "Connected";
    } else {
        document.getElementById("connectionDotStyle").innerHTML = "#connectionDot {background-color: #ed143d;}";
        document.getElementById("connectionState").innerHTML = "Disconnected";
    }
}

function readTag() {
    // loadFilamentData(jsonData)
}

function writeTag() {

}

socket.on("nfc_state", (data) => {
    updateConnectionState(data.reader_connected);
});

socket.on("disconnect", (data) => {
    updateConnectionState(false);
})

setInterval(() => {
    socket.emit("ping");
}, 1000);
