
var new_message = function(data) {
    var chatid = data.chatid;
    if (chatid === undefined) {
        chatid = 'campaign';
    }

    var chat = $('#chat-' + chatid);

    if (data.name == 'system') {
        data.type = 'system';
    }

    var prev = chat.find('.messages .msg-row:last-child');
    var prev_name = prev.find('.name').text();
    var msg;

    if (data.name != 'system' && prev_name == data.name) {
        msg = $(Templates.message(data)).find('.msg')
            .appendTo(prev);
    } else {
        msg = $(Templates.message(data))
            .appendTo(chat.find('.messages'));
    }

    msg.css('opacity', 0)
        .animate({
            opacity: 1
        });

    var elem = $('#chat-campaign .messages')[0];
    elem.scrollTop = elem.scrollHeight;
};

var term_result = function(data) {
    if (data.cmd === true) {
        $(Templates['terminal-cmd'](data))
            .appendTo('#terminal-logs');
    } else {
        $(Templates['terminal-log'](data))
            .appendTo('#terminal-logs');
    }

    var elem = $('#terminal-logs')[0];
    elem.scrollTop = elem.scrollHeight;
};

var new_chat = function(data) {
    var chat = $(Templates['chat'](data));
    $('.chat-group').append(chat);

    if (data.name === undefined) {
        data.name = data.id;
    }

    var btn = $('.chat-btns').append($(Templates['chat-btn'](data)));

    return chat;
};

var switch_chat = function(id) {
    var btns = $('.chat-btn').removeClass('active');
    var btn = btns.filter('[data-id="' + id + '"]')
        .addClass('active');

    var chats = $('.chat').removeClass('active');
    var chat = chats.filter('#chat-' + id)
        .addClass('active');
};


// Reconnection timer
syncrae.retry_timer.listen(function(sec) {
    var timer = $('.connection.timer');
    var time = timer.find('.reconnect-time');

    if (sec <= 0) {
        timer.fadeOut(500);
        time.html('&nbsp;');
        return;
    } else if (timer.is(':hidden')) {
        timer.fadeIn(500);
    }
    time.text(sec);
    format(time);
});

(function() {
    var connected = false;

    syncrae.on(function() {
        connected = true;

        $('.connection').addClass('status-on')
            .removeClass('status-off')
            .removeClass('disabled')
            .filter('.timer')
            .fadeIn(100)
            .find('.reconnect-time')
            .html('&nbsp;');

        // Show a terminal message on websocket connect
        term_result({
            cmd: false,
            level: 'info',
            text: 'websocket connected'
        });
    });
    syncrae.off(function() {
        if (!connected) {
            return; // Don't display the message twice
        }
        connected = false;

        $('.connection').addClass('status-off')
            .removeClass('status-on')
            .removeClass('disabled');

        // Show a Terminal message on websocket disconnect
        term_result({
            cmd: false,
            level: 'warn',
            text: 'websocket disconnected'
        });

        // Show a chat message on websocket disconnect
        new_message({
            name: 'system',
            msg: 'You have been disconnected.'
        });
    });
})();


syncrae.subscribe('/chat/open', function(data) {
    var chat_data = {
        id: data.chatid
    };

    var chat = $('#chat-' + data.chatid);
    if (chat.length === 0) {
        chat = new_chat(chat_data);
    }
});

syncrae.subscribe('/sessions/status', function(data) {
    msgdata = {
        name: 'system'
    };

    if (data.status == 'offline') {
        msgdata['msg'] = data.name + ' just left';
    } else if (data.status == 'online') {
        msgdata['msg'] = data.name + ' just joined us';
    } else {
        console.warn('unknown status: ', data.status);
    }
    new_message(msgdata);
});

// Base handler
syncrae.subscribe('/', function(data) {
    // Adds any errors that are part of the message
    // to the terminal
    if (data.err_code) {
        term_result({
            level: data.level || 'error',
            text: data.err_msg,
            err_code: data.err_code
        });
    }

    if (data.err_code == '5101') {
        // 'Not Logged In' err
        syncrae.retry_timer.disable();
    }
});

syncrae.subscribe('/sessions/error', function(data) {
    new_message({
        name: 'system',
        msg: data.error
    });
});

syncrae.subscribe('/messages/new', function(data) {
    new_message(data);
});

syncrae.subscribe('/terminal/result', function(data) {
    term_result(data);
});

$(function() {
    terminal.elem($('#terminal-input'));
    // auto focus to the chat body when loading the page
    $('#chat-campaign .msg-input').focus();

    // send messages when form is changed
    $('#chat-campaign .msg-form').on('keydown', function(e) {
        if (e.keyCode != 13) {
            return;
        }
        e.preventDefault();

        var data = {
            msg: $(this).find('.msg-input').val()
        };

        // send message
        syncrae.publish('/messages/new', data);

        // reset form
        $(this).find('.msg-input').val('');
    });

    // Global Shortcuts
    var global_keys = {};
    $('body').keydown(function(e) {
        var key = e.keyCode;
        global_keys[key] = true;

        // Main-t
        // Open-close Terminal
        if (global_keys[16] && global_keys[32]) {
            var elem = $('#terminal');
            elem.toggle();
            if (elem.is(':visible')) {
                var last_focused = $(':focus');
                terminal.reloader.save(last_focused);
            } else {
                terminal.reloader.reload();
            }
        } else {
            // Not a global shortcut, continue propogation
            return;
        }
        // If one of the commands was activated then stop default action
        // and any other callbacks
        return false;
    });
    $('body').keyup(function(e) {
        var key = e.keyCode;
        global_keys[key] = undefined;
    });

    $('#terminal').on('click', function() {
        $(this).find('.user-cmd').focus();
    });

    // Terminal submission
    $('#terminal-input .user-cmd').keyup(function(e) {
        var elem = $(this);
        // Enter key
        if (e.keyCode == 13) {
            data = {
                cmd: elem.val()
            };

            // Send command
            syncrae.publish('/terminal/command', data);

            // Clear the input
            elem.val('');
            terminal.history.add(data.cmd);
        // Up
        } else if (e.keyCode == 38) {
            elem.text(terminal.history.next());
        // Down
        } else if (e.keyCode == 40) {
            elem.text(terminal.history.prev());
        } else {
            return;
        }
        return false;
    });

    $('.chat-sidebar').on('click', '.chat-btn', function() {
        var elem = $(this);
        switch_chat(elem.data('id'));
    });
    $('.connection.disc-msg .close').on('click', function() {
         $('.connection.disc-msg').addClass('disabled');
    });
});


