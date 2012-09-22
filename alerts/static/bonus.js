/**
 * Highlights the level text with the proper colour
 */
django.jQuery(function() {
    django.jQuery('#result_list tbody tr').each(function() {
        var item = django.jQuery(
            django.jQuery(this).find('td')[1]
        );
        var val = item.text();
        item.addClass(val);
        item.addClass('text-level');
    });
});


/**
 * Adds a little pill which shows you what the current alert level is
 */
django.jQuery(function() {
    var old_level = django.jQuery('#id_level').val();

    django.jQuery('#id_level').parent().append(
        django.jQuery('<span class="text-level pill ' + old_level + '">!</span>')
    );

    django.jQuery('#id_level').bind('change', function() {
        var $level = django.jQuery('#id_level');
        var level = $level.val();

        if (level != old_level) {
            var pointer = django.jQuery('.pointer');
            if (!pointer.length) {
                $level.parent().append(django.jQuery('<span class="pointer">➤</span>'));
            };

            django.jQuery('.new.pill').remove();
            django.jQuery('#id_level').parent().append(
                django.jQuery('<span class="text-level new pill ' + level + '">!</span>')
            );
        } else {
            django.jQuery('.new.pill').add('.pointer').remove();
        }
    });
});

/**
 * Adds an edit button before the title on each row
 */
django.jQuery(function(){
    // Add another column
    var title_th = django.jQuery(
        django.jQuery('#result_list thead tr th')[1]
    );
    var edit_col = django.jQuery('<th width="5em"></th>');
    edit_col.insertBefore(title_th);


    django.jQuery('#result_list tbody tr').each(function() {
        var item = django.jQuery(this).find('th');
        item.css('border-left', '0px');
        var edit_btn = django.jQuery('<td><a class="edit" href="' + item.find('a').attr('href') + '"> Edit </a></td>');
        edit_btn.insertBefore(item);
    });
});




