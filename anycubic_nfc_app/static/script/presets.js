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
        "speedMinA": "speed_min" in data["range_a"] ? data["range_a"]["speed_min"] : "",
        "speedMaxA": "speed_max" in data["range_a"] ? data["range_a"]["speed_max"] : "",
        "nozzleMinA": data["range_a"]["nozzle_min"],
        "nozzleMaxA": data["range_a"]["nozzle_max"],
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
        document.getElementById(key).value = finalData[key] === 0 ? "" : finalData[key];
    }
}

function loadPreset(type) {
    if(type in presets) {
        loadFilamentData(presets[type])
    }
}

function getIntDefault(inputId, defaultValue) {
    var value = document.getElementById(inputId).value;
    return value == "" ? defaultValue : parseInt(value);
}

function getFilamentData() {
    return {
        "type": typeSelector.value,
        "color": colorInput.value,
        "range_a": {
            "speed_min": getIntDefault("speedMinA", 0),
            "speed_max": getIntDefault("speedMaxA", 0),
            "nozzle_min": getIntDefault("nozzleMinA", 0),
            "nozzle_max": getIntDefault("nozzleMaxA", 0)
        },
        "range_b": {
            "speed_min": getIntDefault("speedMinB", 0),
            "speed_max": getIntDefault("speedMaxB", 0),
            "nozzle_min": getIntDefault("nozzleMinB", 0),
            "nozzle_max": getIntDefault("nozzleMaxB", 0)
        },
        "range_c": {
            "speed_min": getIntDefault("speedMinC", 0),
            "speed_max": getIntDefault("speedMaxC", 0),
            "nozzle_min": getIntDefault("nozzleMinC", 0),
            "nozzle_max": getIntDefault("nozzleMaxC", 0)
        },
        "bed_min": getIntDefault("bedMin", 0),
        "bed_max": getIntDefault("bedMax", 0)
    };
}

typeSelector.addEventListener("change", function(event) {
    loadPreset(event.target.value);
});
