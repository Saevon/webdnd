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
        prev = msg;
    }

    msg.css('opacity', 0)
        .animate({
            opacity: 1
        });

    var elem = $('#chat-campaign .messages')[0];
    elem.scrollTop = elem.scrollHeight;
};

var player_colour = function(uid) {
    var user = webdnd.user(uid);
    if (user !== undefined && user.color) {
        // Remove any old styles
        $('#player-' + uid + '-colors').remove();

        // Render the new styles
        var data = {
            color: user.color,
            color_alt: '#AAB',
            uid: uid
        };
        var styles = Templates['player_colors'](data);

        // Compile the styles using less


        // Add it to the DOM
        $('#player-colors').append(styles);
    }
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
    var uid = data.expected.filter(function(uid) {return uid !== webdnd.user.self();})[0];
    data.uid = uid;
    if (data.name === undefined) {
        data.name = webdnd.user(uid);
    }

    var chat = $(Templates['chat'](data));
    $('.chat-group').append(chat);


    var btn = $('.chat-btns').append($(Templates['chat-btn'](data)));

    return chat;
};

var switch_chat = function(chatid) {
    var btns = $('.chat-btn').removeClass('active');
    var btn = btns.filter('[data-chatid="' + chatid + '"]')
        .addClass('active')
        .removeClass('new-msgs');

    var chats = $('.chat').removeClass('active');
    var chat = chats.filter('#chat-' + chatid)
        .addClass('active')
        .find('.msg-input')
        .focus();
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
    var chat = $('#chat-' + data.chatid);
    if (chat.length === 0) {
        chat = new_chat(data);
    }
});

syncrae.subscribe('/session/update', function(data) {
    var user = webdnd.user(data.uid);

    // TODO: statuses don't work right now
    // var old_status;
    // if (user !== undefined) {
    //     old_status = user.status;
    // }


    webdnd.user.update(data.uid, data);
    user = webdnd.user(data.uid);

    // Update all colors
    if (data.color) {
        player_colour(data.uid);
    }

    // if ((old_status === undefined && user.status !== undefined) ||
    // (old_status !== undefined && old_status != user.status)) {
    //     msgdata = {
    //         name: 'system'
    //     };

    //     if (webdnd.user(data.uid).status == 'offline') {
    //         msgdata['msg'] = webdnd.user(data.uid).name + ' just left';
    //     } else if (webdnd.user(data.uid).status == 'online') {
    //         msgdata['msg'] = webdnd.user(data.uid).name + ' just joined us';
    //     } else {
    //         console.warn('unknown status: ', webdnd.user(data.uid).status);
    //     }
    //     new_message(msgdata);
    // }
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

syncrae.subscribe('/session/error', function(data) {
    new_message({
        name: 'system',
        msg: data.error
    });
});

syncrae.subscribe('/messages/new', function(data) {
    if (data.chatid) {
        // Make sure the new message indicator is showing
        var btn = $('.chat-btn[data-chatid="' + data.chatid + '"]');
        if (!btn.hasClass('active')) {
            btn.addClass('new-msgs');
        }
    }

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
    $('.chat-group').on('keydown', '.msg-input', function(e) {
        if (e.keyCode != 13) {
            return;
        }
        e.preventDefault();

        var elem = $(this);

        var data = {
            msg: elem.val()
        };

        var chatid = elem.parents('.chat').data('chatid');
        data.chatid = chatid;
        data.uid = webdnd.user.self();

        // send message
        syncrae.publish('/messages/new', data);

        // reset form
        elem.val('');
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
        switch_chat(elem.data('chatid'));
    });
    $('.connection.disc-msg .close').on('click', function() {
         $('.connection.disc-msg').addClass('disabled');
    });
});


