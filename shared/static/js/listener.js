
var new_message = function(data) {
    if (data.name == 'system') {
        if (data.type === undefined) {
            data.type = 'notification';
        }
    }

    var message = $(Mustache.templates.message(data))
        .css('opacity', 0)
        .css('position', 'relative')
        .css('left', '-200px')
        .appendTo('#messages')
        .animate({
            opacity: 1,
            left: 0
        });

    var elem = $('#messages')[0];
    elem.scrollTop = elem.scrollHeight;
};

var term_result = function(data) {
    if (data.cmd === true) {
        $(Mustache.templates['terminal-cmd'](data))
            .appendTo('#terminal-logs');
    } else {
        $(Mustache.templates['terminal-log'](data))
            .appendTo('#terminal-logs');
    }

    var elem = $('#terminal-logs')[0];
    elem.scrollTop = elem.scrollHeight;
};


// Reconnection timer
syncrae.retry_timer.listen(function(sec) {
    var timer = $('.connection');
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
            .fadeIn(100)
            .find('.reconnect-time')
            .html('&nbsp;');

        // Show a terminal message on websocket connect
        term_result({
            cmd: false,
            level: 'info',
            log: 'websocket connected'
        });
    });
    syncrae.off(function() {
        if (!connected) {
            return; // Don't display the message twice
        }
        connected = false;

        $('.connection').addClass('status-off')
            .removeClass('status-on');

        // Show a Terminal message on websocket disconnect
        term_result({
            cmd: false,
            level: 'warn',
            log: 'websocket disconnected'
        });
    });
})();

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

syncrae.subscribe('/sessions/error', function(data) {
    term_result({
        level: data.level || 'error',
        log: data.error
    });
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
    // auto focus to the chat body when loading the page
    $('#msg-input').focus();

    // send messages when form is changed
    $('#msg-form').submit(function(e) {
        e.preventDefault();

        var data = {
            msg: $(this).find('#msg-input').val()
        };

        // send message
        syncrae.publish('/messages/new', data);

        // reset form
        $(this).find('#msg-input').val('');
    });

    // Global Shortcuts
    var global_keys = {};
    $('body').keydown(function(e) {
        global_keys[e.keyCode] = true;

        // Ctrl-t
        // Open-close Terminal
        if (global_keys[17] && global_keys[84]) {
            terminal = $('#terminal');
            terminal.toggle();
            if (terminal.is(':visible')) {
                terminal.find('#terminal-input .user-cmd').focus();
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
        global_keys[e.keyCode] = undefined;
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
                cmd: elem.text()
            };

            // Send command
            syncrae.publish('/terminal/command', data);

            // Clear the input
            elem.text('');
        }
    });
});


