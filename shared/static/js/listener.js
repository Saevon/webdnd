syncrae.subscribe('/sessions/new', function(data) {
    data = {name: 'system', body: data.name + ' just joined us'};
    $(Handlebars.templates.message(data))
        .addClass('notification')
        .css('opacity', 0)
        .appendTo('#messages')
        .animate({
            opacity: 1
        });
});

syncrae.subscribe('/sessions/key', function(data) {
    syncrae.user.key(data.key);
    syncrae.queue.keyed();
    console.log("new key: ", data.key);
});

syncrae.subscribe('/sessions/name', function(data) {
    syncrae.user.name(data.name);
    syncrae.user.cname(data.cname);
    $('.type .name').text(syncrae.user.name());
    $('head title').text(syncrae.user.cname());
});

syncrae.subscribe('/sessions/error', function(data) {
    data = {
        name: 'system',
        body: data.error
    };
    var message = $(Handlebars.templates.message(data))
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
    var message = $(Handlebars.templates.message(data))
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
    data = {name: data['name'], body: 'started typing...'};
    $(Handlebars.templates.message(data))
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
    syncrae.user.name('anon');

    // auto focus to the chat body when loading the page
    $('#form input[name=body]').focus();

    // send messages when form is changed
    $('#form form').submit(function(e) {
        e.preventDefault();

        // notify that typing has stopped
        syncrae.publish('/messages/stopped-typing', {
            name: syncrae.user.name()
        });

        var data = {
            name: syncrae.user.name(),
            body: $(this).find('input[name=body]').val()
        };

        // send message
        syncrae.publish('/messages/new', data);

        // reset form
        $(this).find('input[name=body]').val('');
    });

    // track typing
    var typing = false;
    $('#form input[name=body]').keyup(function(e) {
        // notify that typing has started
        if (typing && $(this).val().length === 0) {
            typing = false;
            syncrae.publish('/messages/stopped-typing', {
                name: syncrae.user.name()
            });
        } else if (!typing && $(this).val().length > 0) {
            typing = true;
            syncrae.publish('/messages/started-typing', {
                name: syncrae.user.name()
            });
        }
    });

});
