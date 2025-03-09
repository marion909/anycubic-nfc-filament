var presets = {};
const typeSelector = document.getElementById("type");

function updatePresets(filamentPresets) {
    presets = filamentPresets;
    loadPreset("PLA");
}

function loadPreset(type) {
    if(!(type in presets)) {
        return;
    }
    var preset = presets[type];
    var finalData = {
        "bedMin": "bed_min" in preset ? preset["bed_min"] : "",
        "bedMax": "bed_max" in preset ? preset["bed_max"] : "",
        "speedMinA": ("range_a" in preset && "speed_min" in preset["range_a"]) ? preset["range_a"]["speed_min"] : "",
        "speedMaxA": ("range_a" in preset && "speed_max" in preset["range_a"]) ? preset["range_a"]["speed_max"] : "",
        "nozzleMinA": ("range_a" in preset && "nozzle_min" in preset["range_a"]) ? preset["range_a"]["nozzle_min"] : "",
        "nozzleMaxA": ("range_a" in preset && "nozzle_max" in preset["range_a"]) ? preset["range_a"]["nozzle_max"] : "",
        "speedMinB": ("range_b" in preset && "speed_min" in preset["range_b"]) ? preset["range_b"]["speed_min"] : "",
        "speedMaxB": ("range_b" in preset && "speed_max" in preset["range_b"]) ? preset["range_b"]["speed_max"] : "",
        "nozzleMinB": ("range_b" in preset && "nozzle_min" in preset["range_b"]) ? preset["range_b"]["nozzle_min"] : "",
        "nozzleMaxB": ("range_b" in preset && "nozzle_max" in preset["range_b"]) ? preset["range_b"]["nozzle_max"] : "",
        "speedMinC": ("range_c" in preset && "speed_min" in preset["range_c"]) ? preset["range_c"]["speed_min"] : "",
        "speedMaxC": ("range_c" in preset && "speed_max" in preset["range_c"]) ? preset["range_c"]["speed_max"] : "",
        "nozzleMinC": ("range_c" in preset && "nozzle_min" in preset["range_c"]) ? preset["range_c"]["nozzle_min"] : "",
        "nozzleMaxC": ("range_c" in preset && "nozzle_max" in preset["range_c"]) ? preset["range_c"]["nozzle_max"] : "",
    };
    if(typeSelector.value != type) {
        typeSelector.value = type;
    }
    for (const key in finalData) {
        document.getElementById(key).value = finalData[key];
    }
}

typeSelector.addEventListener("change", function(event) {
    loadPreset(event.target.value);
});
