/**
 * Created by mark on 7/1/16.
 */

/* Global settings for GUI */
var fontSize = 15;
var justify = false;

/* Counter */
counter = function () {
    var value = $('#textArea').val();

    if (value.length == 0) {
        $('#wordCount').html(0);
        return;
    }

    var regex = /\s+/gi;
    var wordCount = value.trim().replace(regex, ' ').split(' ').length;

    $('#wordCount').html(wordCount);
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

loadPage = function (caretPos, scrollTop, fontSizeFromServer) {
    $('#textArea').css({"font-size": fontSizeFromServer + "px"});
    $('#textArea')[0].selectionStart = caretPos;
    fontSize = fontSizeFromServer;
    prettyFontButtons();

    // This is so weird only works if its shifted down
    $('#textArea').scrollTop(scrollTop);
    $('#textArea').focus();
};

/* GUI functions */
toggleJustify = function () {
    if (!justify) {
        $('#textArea').css({"text-align": "justify"});
        $('#justifyIcon').removeClass("md-inactive");

    } else {
        $('#textArea').css({"text-align": "left"});
        $('#justifyIcon').addClass("md-inactive");
    }
    justify = !justify;
};

toggleFont = function (inc) {
    if (inc) {
        if (fontSize < 30) fontSize += 1;
    } else {
        if (fontSize > 10) fontSize -= 1;
    }
    prettyFontButtons();
    $('#textArea').css({"font-size": fontSize + "px"});
};

prettyFontButtons = function () {
    if (fontSize == 10) {
        $('#fontDec').addClass("md-inactive");
    } else if (fontSize == 30) {
        $('#fontInc').addClass("md-inactive");
    } else {
        $('#fontInc').removeClass("md-inactive");
        $('#fontDec').removeClass("md-inactive");
    }
};

/* Saving to the server */
saveContent = function () {
    var content = $('#textArea').val();
    var caretPos = $('#textArea')[0].selectionStart;
    var scrollTop = $('#textArea')[0].scrollTop;
    var data = {
        "content": content,
        "caretPos": caretPos,
        "scrollTop": scrollTop,
        "fontSize": fontSize
    };
    $.post(window.location.href, data);
    return false;
};