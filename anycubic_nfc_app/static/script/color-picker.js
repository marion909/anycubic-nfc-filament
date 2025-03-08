function initColorPicker(pickerId, inputId, hexColor) {
    document.getElementById(inputId).value = hexColor;

    // Initialize Pickr
    const pickr = Pickr.create({
        el: '#' + pickerId,
        theme: 'monolith',
        default: hexColor,
        defaultRepresentation: 'HEX',
        position: 'bottom-start',
        adjustableNumbers: false,
        swatches: [
            '#212721',
            '#8A8D8F',
            '#D0CFCA',
            '#FFFFFF',
            '#E10600',
            '#F88192',
            '#CF4F80',
            '#FF7338',
            '#695FA2',
            '#3E55AB',
            '#3DB24E',
            '#75CB5D',
            '#FDDB27',
            '#7C4D3A',
            '#927968',
            '#D4B996',
            '#23A3C7'
        ],
        components: {
            preview: true,
            opacity: false,
            hue: true,
            interaction: {
                hex: false,
                rgba: false,
                input: true,
                save: true
            }
        },
        i18n: {
            'btn:save': '✓'
        }
    });

    // Update hidden input on color change
    pickr.on('save', (color) => {
        document.getElementById(inputId).value = color.toHEXA().toString();
    });
}

initColorPicker("colorPickerA", "colorInputA", "#E10600");
initColorPicker("colorPickerB", "colorInputB", "#75CB5D");
initColorPicker("colorPickerC", "colorInputC", "#23A3C7");
