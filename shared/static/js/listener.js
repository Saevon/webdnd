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

});
