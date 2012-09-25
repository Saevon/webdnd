$(function() {
    /*****************************
     * Alerts dismissal by clicking on any part of them
     * Only alerts with a 'close' button can be closed this way
     *   aka with a data-dismiss attr
     */

    // Currently disabled .: dblotsky doesn't want it :(

    // $('.alert').on('click', function() {
    //     $(this).alert('close')
    // });

    // var old_alert = $.fn.alert;

    // $.fn.alert = function alert(opt) {
    //     // Hijack new alerts that have a close button
    //     if (opt === undefined && $(this).find('[data-dismiss]').length) {
    //         $(el).on('click', function() {
    //             $(this).alert('close');
    //         });
    //     };
    //     return old_alert.call(this, opt);
    // }
});
