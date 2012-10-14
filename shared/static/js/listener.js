syncrae.subscribe('/sessions/new', function(data) {
    data = {
        name: 'system',
        msg: data.name + ' just joined us'
    };
    $(Mustache.templates.message(data))
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
    $(Mustache.templates['terminal-cmd'](data))
        .appendTo('#terminal-logs');
    $(Mustache.templates['terminal-log'](data))
        .appendTo('#terminal-logs');

    var elem = $('#terminal-logs')[0];
    elem.scrollTop = elem.scrollHeight;
});

syncrae.subscribe('/messages/started-typing', function(data) {
    // handle started typing
    data = {
        name: data['name'],
        msg: 'started typing...'
    };
    $(Mustache.templates.message(data))
        .addClass('typing')
        .css('opacity', 0)
        .appendTo('#messages')
        .animate({
            opacity: 1
        });
});

syncrae.subscribe('/messages/stopped-typing', function(data) {
   $('.typing').remove();
});

$(function() {
    // auto focus to the chat body when loading the page
    $('#form input[name=msg]').focus();

    // send messages when form is changed
    $('#form form').submit(function(e) {
        e.preventDefault();

        // notify that typing has stopped
        syncrae.publish('/messages/stopped-typing');

        var data = {
            msg: $(this).find('input[name=msg]').val()
        };

        // send message
        syncrae.publish('/messages/new', data);

        // reset form
        $(this).find('input[name=msg]').val('');
    });

    // track typing
    var typing = false;
    $('#form input[name=msg]').keyup(function(e) {
        // notify that typing has started
        if (typing && $(this).val().length === 0) {
            typing = false;
            syncrae.publish('/messages/stopped-typing');
        } else if (!typing && $(this).val().length > 0) {
            typing = true;
            syncrae.publish('/messages/started-typing');
        }
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

    // Terminal submition
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



