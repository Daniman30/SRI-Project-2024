// Muestra las configuraciones o el listado de resultados en dependencia de lo que este seleccionado
document.getElementById('config-button').addEventListener('click', function() {
    var configOptions = document.getElementById('config-options');
    var searchResults = document.getElementById('search-results');

    if (configOptions.classList.contains('hidden')) {
        configOptions.classList.remove('hidden');
        searchResults.classList.add('hidden');
    } else {
        configOptions.classList.add('hidden');
        searchResults.classList.remove('hidden');
    }
});


document.getElementById('search-form').addEventListener('submit', function(event) {
    // Check if the custom values ​​checkbox is enabled
    var option1 = document.getElementById('option1');
    if (option1.checked) {
        var hiddenField = document.createElement('input');
        hiddenField.type = 'hidden';
        hiddenField.name = 'option1';
        hiddenField.value = 'true';
        this.appendChild(hiddenField);
    }

    // Check if the query expand checkbox is on
    if (query_expand_bool.checked) {
        var hiddenField = document.createElement('input');
        hiddenField.type = 'hidden';
        hiddenField.name = 'query_expand_bool';
        hiddenField.value = 'true';
        this.appendChild(hiddenField);
    }

    // Check if the stop words checkbox is on
    if (stop_words_bool.checked) {
        var hiddenField = document.createElement('input');
        hiddenField.type = 'hidden';
        hiddenField.name = 'stop_words_bool';
        hiddenField.value = 'true';
        this.appendChild(hiddenField);
    }

    // Check if the Porter stemmer checkbox is on
    if (stemmer_bool.checked) {
        var hiddenField = document.createElement('input');
        hiddenField.type = 'hidden';
        hiddenField.name = 'stemmer_bool';
        hiddenField.value = 'true';
        this.appendChild(hiddenField);
    }

    // Create a slide for each word in the query
    var query = document.querySelector('input[name="search"]').value;
    var words = query.split(' ');
    var sliderValues = [];

    words.forEach(function(word, index) {
        var slider = document.getElementById('slider-' + index);
        if (slider) {
            sliderValues.push(slider.value);
        }
    });

    var sliderField = document.createElement('input');
    sliderField.type = 'hidden';
    sliderField.name = 'sliders';
    sliderField.value = JSON.stringify(sliderValues);
    this.appendChild(sliderField);
});

// Manages the operation of slides (sliding value bars)
document.querySelector('input[name="search"]').addEventListener('input', function() {
    var query = this.value;
    var words = query.split(' ');
    var slidersContainer = document.getElementById('sliders-container');
    slidersContainer.innerHTML = '';

    words.forEach(function(word, index) {
        var sliderLabel = document.createElement('label');
        sliderLabel.textContent = `Valor del Slider para "${word}" (-1 a 1): `;
        var sliderValue = document.createElement('span');
        sliderValue.id = 'slider-value-' + index;
        sliderValue.textContent = '0';

        var slider = document.createElement('input');
        slider.type = 'range';
        slider.id = 'slider-' + index;
        slider.name = 'slider-' + index;
        slider.min = '-1';
        slider.max = '1';
        slider.step = '0.01';
        slider.value = '0';
        slider.addEventListener('input', function() {
            sliderValue.textContent = this.value;
        });

        slidersContainer.appendChild(sliderLabel);
        slidersContainer.appendChild(sliderValue);
        slidersContainer.appendChild(slider);
        slidersContainer.appendChild(document.createElement('br'));
    });
});

// Store initial values ​​of sliders
var initialSliderValues = [];
document.querySelectorAll('input[type="range"]').forEach(function(slider, index) {
    initialSliderValues.push(slider.value);
});

// Handling slider reset
document.getElementById('reset-button').addEventListener('click', function() {
    document.querySelectorAll('input[type="range"]').forEach(function(slider, index) {
        slider.value = initialSliderValues[index];
        document.getElementById('slider-value-' + index).textContent = initialSliderValues[index];
    });
});

// If the original values ​​of the slides were modified
// generates a reset button to update them to their previous values
document.getElementById('option1').addEventListener('change', function() {
    var slidersContainer = document.getElementById('sliders-container');
    var resetButton = document.getElementById('reset-button');
    
    if (this.checked) {
        slidersContainer.style.display = 'block';
        resetButton.style.display = 'block';
    } else {
        slidersContainer.style.display = 'none';
        resetButton.style.display = 'none';
    }
});

// Show slides and reset button only if custom values ​​checkbox is active
window.onload = function() {
    var option1 = document.getElementById('option1');
    var slidersContainer = document.getElementById('sliders-container');
    var resetButton = document.getElementById('reset-button');
    
    if (!option1.checked) {
        slidersContainer.style.display = 'none';
        resetButton.style.display = 'none';
    }
};


