/*
Field Highlighter Module
Authors: Serghei Filippov, Saevon
Created: Sept 22nd 2012

Requirements: Twitter Bootstrap, Highlighter extra css

This module creates a function that allows you to easily highlight a
control-group, adding a message. Thus you can have your froms highlight
erroneous fields after submission

Usage:

alerts.highlight('CSS SELECTOR', 'LEVEL', 'OPTIONAL TEXT');
    CSS SELECTOR:
        Any css selector that returns '.control-group' elements
    LEVEL:
        One of the levels listed below, this determines the coloring
    TEXT:
        Optional '.help-inline' text that will be added at the end of your
        inputs. Any previous '.help-inline' will be removed, unless you didn't
        pass in this param.
*/

var alerts = alerts || {};

alerts.highlight = (function() {
    var HIGHLIGHT_LEVELS = [
        'muted',
        'disabled',
        'info',
        'success',
        'warning',
        'error'
    ];

    var highlight = function highlight(selector, level, text) {
        var groups = $(selector);

        // Allow non-unique selectors
        groups.each(function() {
            var group = $(this)

            var inputs = group.find('input');
            inputs.add(group.find('select'))
            inputs.add(group.find('textarea'));

            // Muted means we disable everything in the group
            if (level == 'muted' || level == 'disabled') {
                inputs.addClass('disabled').addClass('muted')
                    .prop('disabled', true);
            } else {
                inputs.removeClass('disabled').removeClass('muted')
                    .prop('disabled', false);
                }

            // Make text optional, and always add it at the end of the group
            if (text !== undefined) {
                // Remove any old help text
                var old = inputs.last().next();
                if (old && old.hasClass('help-inline')) {
                    old.remove();
                }

                var help_text = $('<span class="help-inline">' + text + '</span>');
                inputs.last().after(help_text);
            }
        });

        // Remove add then re-add the highlight level
        var length = HIGHLIGHT_LEVELS.length;
        for (var i=0; i < length; i++) {
            groups.removeClass(HIGHLIGHT_LEVELS[i]);
        }
        groups.addClass(level);

        return groups;
    };

    return highlight;
})();



