const socket = io();
var canceled = false;

function downloadTextFile(filename, content) {
    const blob = new Blob([content], { type: "text/plain" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(link.href);
}

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
    if(document.getElementById("spoolForm").reportValidity()) {
        updateNFCOverlay(true);
        socket.emit("write_tag", getFilamentData());
    }
}

function createDump() {
    updateNFCOverlay(true);
    socket.emit("create_dump");
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

socket.on("write_done", (data) => {
    if(canceled) {
        // Ignore if canceled
        canceled = false;
        return;
    }
    if(data.success) {
        updateNFCOverlay(false);
    } else {
        updateNFCOverlay(true, true);
        socket.emit("write_tag", getFilamentData());
    }
})

socket.on("dump_done", (data) => {
    if(canceled) {
        // Ignore if canceled
        canceled = false;
        return;
    }
    if(data.success) {
        downloadTextFile(data.filename, data.data);
        updateNFCOverlay(false);
    } else {
        updateNFCOverlay(true, true);
        socket.emit("create_dump");
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
