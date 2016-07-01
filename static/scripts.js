/**
 * Created by mark on 7/1/16.
 */

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

load_page = function (caretPos, scrollTop) {
    counter();
    $('#textArea')[0].scrollTop = scrollTop;
    $('#textArea')[0].selectionStart = caretPos;
};

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
    var content = $('#textArea').val();
    var caretPos = $('#textArea')[0].selectionStart;
    var scrollTop = $('#textArea')[0].scrollTop;
    var data = {
        "content": content,
        "caretPos": caretPos,
        "scrollTop": scrollTop
    };
    $.post("../save_post", data);
    return false;
};