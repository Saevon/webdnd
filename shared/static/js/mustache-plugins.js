

Mustache.prefix = '{{=<% %>=}}';

/**
 * Forces a hook during render and compile that changes the default delims
 */
Mustache.render = (function() {
    var old_render = Mustache.render;

    var render = function(template, params) {
        return old_render(Mustache.prefix + template, params);
    };

    return render;
})();

Mustache.compile = (function() {
    var old_compile = Mustache.compile;

    var compile = function(template, tags) {

        return old_compile(Mustache.prefix + template, tags);
    };

    return compile;
})();

// Prepare dict to store compiled templates
Mustache.templates = {};
