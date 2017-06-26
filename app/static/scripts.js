function translate(sourceLang, destLang, sourceId, destId, loadingId) {
    $(destId).hide();
    $(loadingId).show();
    $.post('/translate', {
        text: $(sourceId).text(),
        sourceLang: sourceLang,
        destLang: destLang
    }).done(function(translated) {
        $(destId).text(translated['text'])
        $(loadingId).hide();
        $(destId).show();
    }).fail(function() {
        $(destId).text("{{ _('Error: Could not contact server.') }}");
        $(loadingId).hide();
        $(destId).show();
    });
}

/* changes datetime html to work with placeholders*/

window.onload = function () {
    /* Grab all elements with a placeholder attribute */
    var element = document.querySelectorAll('[placeholder]');

    /* Loop through each found elements */
    for (var i in element) {
        /* If the element is a DOMElement and has the nodeName "INPUT" */
        if (element[i].nodeType == 1 && element[i].nodeName == "INPUT") {

            /* We change the value of the element to its placeholder attr value */
            element[i].value = element[i].getAttribute('placeholder');
            /* We change its color to a light gray */
            element[i].style.color = "#777";

            /* When the input is selected/clicked on */
            element[i].onfocus = function (event) {
                /* If the value within it is the placeholder, we clear it */
                if (this.value == this.getAttribute('placeholder')) {
                    this.value = "";
                    /* Setting default text color */
                    this.style.color = "#000";
                };
            };

            /* We the input is left */
            element[i].onblur = function (event) {
                /* If the field is empty, we set its value to the placeholder */
                if (this.value == "") {
                    this.value = this.getAttribute('placeholder');
                    this.style.color = "#777";
                }
            };
        }
    }
}
