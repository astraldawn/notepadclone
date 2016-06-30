/**
 * Created by mark on 7/1/16.
 */

/* Counter */
counter = function () {
    var value = $('#textArea').val();

    if (value.length == 0) {
        $('#wordCount').html(0);
        $('#caretPos').html(0);
        $('#scrollTop').html(0);
        return;
    }

    var regex = /\s+/gi;
    var wordCount = value.trim().replace(regex, ' ').split(' ').length;
    var caretPos = $('#textArea')[0].selectionStart;
    var scrollTop = $('#textArea')[0].scrollTop;

    $('#wordCount').html(wordCount);
    $('#caretPos').html(caretPos);
    $('#scrollTop').html(scrollTop);
};

$(document).ready(function () {
    $('#textArea').change(counter);
    $('#textArea').keydown(counter);
    $('#textArea').keypress(counter);
    $('#textArea').keyup(counter);
    $('#textArea').blur(counter);
    $('#textArea').focus(counter);
    $('#textArea').mousedown(counter);
    $('#textArea').mouseup(counter);
    $('#textArea').scroll(counter);
});

/* GUI functions */
var justify = false;

toggleJustify = function () {
    if (!justify) {
        $('#textArea').css({"text-align": "justify"});
    } else {
        $('#textArea').css({"text-align": "left"});
    }
    justify = !justify;
};

/* Saving to the server */
saveContent = function () {
    alert("Saves content to server");
    return false;
};