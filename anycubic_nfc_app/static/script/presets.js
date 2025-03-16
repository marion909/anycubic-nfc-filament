var presets = {};
const typeSelector = document.getElementById("type");

function updatePresets(filamentPresets) {
    presets = filamentPresets;
    loadPreset("PLA");
}

function loadFilamentData(data) {
    var finalData = {
        "bedMin": "bed_min" in data ? data["bed_min"] : "",
        "bedMax": "bed_max" in data ? data["bed_max"] : "",
        "speedMinA": ("range_a" in data && "speed_min" in data["range_a"]) ? data["range_a"]["speed_min"] : "",
        "speedMaxA": ("range_a" in data && "speed_max" in data["range_a"]) ? data["range_a"]["speed_max"] : "",
        "nozzleMinA": ("range_a" in data && "nozzle_min" in data["range_a"]) ? data["range_a"]["nozzle_min"] : "",
        "nozzleMaxA": ("range_a" in data && "nozzle_max" in data["range_a"]) ? data["range_a"]["nozzle_max"] : "",
        "speedMinB": ("range_b" in data && "speed_min" in data["range_b"]) ? data["range_b"]["speed_min"] : "",
        "speedMaxB": ("range_b" in data && "speed_max" in data["range_b"]) ? data["range_b"]["speed_max"] : "",
        "nozzleMinB": ("range_b" in data && "nozzle_min" in data["range_b"]) ? data["range_b"]["nozzle_min"] : "",
        "nozzleMaxB": ("range_b" in data && "nozzle_max" in data["range_b"]) ? data["range_b"]["nozzle_max"] : "",
        "speedMinC": ("range_c" in data && "speed_min" in data["range_c"]) ? data["range_c"]["speed_min"] : "",
        "speedMaxC": ("range_c" in data && "speed_max" in data["range_c"]) ? data["range_c"]["speed_max"] : "",
        "nozzleMinC": ("range_c" in data && "nozzle_min" in data["range_c"]) ? data["range_c"]["nozzle_min"] : "",
        "nozzleMaxC": ("range_c" in data && "nozzle_max" in data["range_c"]) ? data["range_c"]["nozzle_max"] : "",
    };
    var type = "type" in data ? data["type"] : "PLA";
    if(typeSelector.value != type) {
        typeSelector.value = type;
    }
    if("color" in data) {
        setColor(data["color"]);
    }
    for (const key in finalData) {
        document.getElementById(key).value = finalData[key];
    }
}

function loadPreset(type) {
    if(type in presets) {
        loadFilamentData(presets[type])
    }
}

typeSelector.addEventListener("change", function(event) {
    loadPreset(event.target.value);
});
