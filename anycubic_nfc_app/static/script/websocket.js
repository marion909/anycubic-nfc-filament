function setConnectionState(connected) {
    if(connected) {
        document.getElementById("connectionDotStyle").innerHTML = "";
        document.getElementById("connectionState").innerHTML = "Connected";
    } else {
        document.getElementById("connectionDotStyle").innerHTML = "#connectionDot {background-color: #ed143d;}";
        document.getElementById("connectionState").innerHTML = "Disconnected";
    }
}
