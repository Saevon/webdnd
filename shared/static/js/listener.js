
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

syncrae.on(function() {
    $('.connection').addClass('status-on')
        .removeClass('status-off')
        .fadeIn(100);

    // Show a terminal message on websocket connect
    $(Mustache.templates['terminal-log']({
        level: 'info',
        log: 'websocket connected'
    })).appendTo('#terminal-logs');

    var elem = $('#terminal-logs')[0];
    elem.scrollTop = elem.scrollHeight;
});
syncrae.off(function() {
    $('.connection').addClass('status-off')
        .removeClass('status-on');

    // Show a Terminal message on websocket disconnect
    $(Mustache.templates['terminal-log']({
        level: 'warn',
        log: 'websocket disconnected'
    })).appendTo('#terminal-logs');

    var elem = $('#terminal-logs')[0];
    elem.scrollTop = elem.scrollHeight;
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
    $(Mustache.templates.message(msgdata))
        .addClass('notification')
        .css('opacity', 0)
        .appendTo('#messages')
        .animate({
            opacity: 1
        });
});

syncrae.subscribe('/sessions/error', function(data) {
    data = {
        name: 'system',
        msg: data.error
    };
    var message = $(Mustache.templates.message(data))
        .css('opacity', 0)
        .css('position', 'relative')
        .css('left', '-200px')
        .appendTo('#messages')
        .animate({
            opacity: 1,
            left: 0
        });

});

syncrae.subscribe('/messages/new', function(data) {
    // idea... if the message comes from you it should
    // slide in from the bottom up
    // if it comes from someone else it slides in from the side
    var message = $(Mustache.templates.message(data))
        .css('opacity', 0)
        .css('position', 'relative')
        .css('left', '-200px')
        .appendTo('#messages')
        .animate({
            opacity: 1,
            left: 0
        });
});

syncrae.subscribe('/terminal/result', function(data) {
    if (data.cmd === true) {
        $(Mustache.templates['terminal-cmd'](data))
            .appendTo('#terminal-logs');
    } else {
        $(Mustache.templates['terminal-log'](data))
            .appendTo('#terminal-logs');
    }

    var elem = $('#terminal-logs')[0];
    elem.scrollTop = elem.scrollHeight;
});

$(function() {
    // auto focus to the chat body when loading the page
    $('#form input[name=msg]').focus();

    // send messages when form is changed
    $('#form form').submit(function(e) {
        e.preventDefault();

        var data = {
            msg: $(this).find('input[name=msg]').val()
        };

        // send message
        syncrae.publish('/messages/new', data);

        // reset form
        $(this).find('input[name=msg]').val('');
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
                terminal.find('#terminal-cmd').focus();
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

    // Terminal submission
    $('#terminal-cmd').keyup(function(e) {
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
        }
    });
});


