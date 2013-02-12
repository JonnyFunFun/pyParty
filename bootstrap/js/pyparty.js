String.prototype.f = function() {
    var s = this, i = arguments.length;
    console.log(arguments.length);
    while (i--)
        s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
    return s;
};

function sendChatMessage(msg) {
    $.ajax({
        type: 'POST',
        data: {message:msg},
        url: '/chat/post/',
        dataType: 'json',
        success: function(data) {
            console.log(data);
            if (data.success == true) {
                $('div#chat_message_box').append(data.child);
            } else {
                //TODO: some message about a chat not being sent?
            }
        }
    })
}

function syncChatMessages() {
    /* gather the last received message */
    var last_message = $('div#chat_message_box > div:last').attr('data-id');
    $.ajax({
        type: 'POST',
        data: {last:last_message},
        url: '/chat/sync/',
        dataType: 'json',
        success: function(data) {
            if (data.success == true) {
                for (var i=0;i<data.messages.length;i++)
                    $('div#chat_message_box').append(data.messages[i]);
            }
        }
    });
    setTimeout(syncChatMessages, 2000);
}

var ME;

$(document).ready(function() {
    ME = $('span#me_name').html();
    $('textarea#chat_message_input').keypress(function(e) {
        if (e.keyCode == 13) /* enter key */ {
            /* send the chat message */
            var message = $(this).val();
            sendChatMessage(message);
            $(this).val(null);
        }
    });
    setTimeout(syncChatMessages, 2000);
});

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});