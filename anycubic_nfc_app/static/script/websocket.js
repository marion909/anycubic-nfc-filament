const socket = io();
var canceled = false;

function updateConnectionState(connected) {
    if(connected) {
        document.getElementById("connectionDotStyle").innerHTML = "";
        document.getElementById("connectionState").innerHTML = "Connected";
    } else {
        document.getElementById("connectionDotStyle").innerHTML = "#connectionDot {background-color: #ed143d;}";
        document.getElementById("connectionState").innerHTML = "Disconnected";
    }
}

function updateNFCOverlay(show, showError=false) {
    var body = document.getElementById('body');
    var overlay = document.getElementById('backdrop');
    var error = document.getElementById('nfcError');
    if(show) {
        body.style = "overflow: hidden";
        window.scrollTo(0, 0);
        if(showError) {
            error.style = "";
        } else {
            error.style = "display: none;";
        }
        overlay.style = "";
    } else {
        body.style = "";
        overlay.style = "display: none;";
    }
}

function readTag() {
    updateNFCOverlay(true);
    socket.emit("read_tag");
}

function writeTag() {
    updateNFCOverlay(true);
    // socket.emit("write_tag", {});
    // TODO
}

function cancelNFC() {
    socket.emit("cancel_nfc");
}

socket.on("nfc_state", (data) => {
    updateConnectionState(data.reader_connected);
});

socket.on("read_done", (data) => {
    if(canceled) {
        // Ignore if canceled
        canceled = false;
        return;
    }
    if(data.success) {
        loadFilamentData(data.data);
        updateNFCOverlay(false);
    } else {
        updateNFCOverlay(true, true);
        socket.emit("read_tag");
    }
});

socket.on("canceled", (data) => {
    // Note canceled action
    canceled = true;
    updateNFCOverlay(false);
})

socket.on("disconnect", (data) => {
    updateConnectionState(false);
})

setInterval(() => {
    socket.emit("ping");
}, 1000);
