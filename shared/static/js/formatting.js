/**
 * Formats all descendants of the given selector
 */
var format = function format(elem) {
    elem = $(elem);

    var subelem;

    //---------------------------
    //----- Text Formatting -----
    //---------------------------
    subelem = elem.find('.capitalize');
    if (subelem){
        subelem.each(function() {
            item = $(this);
            item.text(format.capitalize(item.text()));
        });
    }

    subelem = elem.find('.lower');
    if (subelem){
        subelem.each(function() {
            item = $(this);
            item.text(item.text().toLowerCase());
        });
    }

    subelem = elem.find('.upper');
    if (subelem){
        subelem.each(function() {
            item = $(this);
            item.text(item.text().toUpperCase());
        });
    }

    //-----------------------------
    //----- Number Formatting -----
    //-----------------------------
    subelem = elem.find('.number');
    if (subelem) {
        subelem.each(function() {
            item = $(this);
            precision = format.cnums(item, 'precise-');
            thousands = !item.hasClass('no-thousands');
            item.text(format.number(item.text(), precision, thousands));
        });
    }

    subelem = elem.find('.percent');
    if (subelem) {
        subelem.each(function() {
            item = $(this);
            precision = format.cnums(item, 'precise-');
            item.text(format.percent(item.text(), precision));
        });
    }

    subelem = elem.find('.currency');
    if (subelem) {
        subelem.each(function() {
            item = $(this);
            allow_cents = !item.hasClass('no-cents');
            shorten = !item.hasClass('no-sa-cents');
            item.text(format.currency(item.text(), allow_cents, shorten));
        });
    }

    subelem = elem.find('.gp');
    if (subelem) {
        subelem.each(function() {
            item = $(this);
            item.html(format.pieces(item.text()));
        });
    }

};


//---------------------------
//----- Text Formatting -----
//---------------------------
format.capitalize = function capitalize(text) {
    text = text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
    text = text.replace(/_/g,' ');
    return text;
};


//-----------------------------
//----- Number Formatting -----
//-----------------------------
format.number = function number(num, precision, thousands_sep) {
    precision = parseInt(precision, 10) || 0;

    num = parseFloat(num).toFixed(precision);
    if (!thousands_sep) {
        return num;
    }

    // Temporarily remove the decimal
    parts = (num + '').split('.');
    num = parts[0];

    // Add commas
    var integer = '';
    var group = '';
    while (num.length >= 4) {
        group = num.substr(num.length - 3, num.length);
        num = num.substr(0, num.length - 3);

        integer = ',' + group + integer;
    }
    integer = num + integer;

    // Re-add the decimal
    if (parts[1] !== undefined) {
        integer = integer + '.' + parts[1];
    }

    return integer;
};

format.currency = function currency(num, allow_cents, shorten) {
    shorten = shorten !== undefined ? shorten : true;
    allow_cents = allow_cents !== undefined ? allow_cents : true;
    // Format cents differently
    if (allow_cents && shorten && parseFloat(num) <= 1.00) {
        var text = format.number(num, 2);
        text = text.substring(2);

        return text + ' ¢';
    }

    return '$' + format.number(num, (allow_cents ? 2 : 0), true);
};

format.percent = function percent(num, precision) {
    return format.number(num, precision) + '%';
};

/**
 * formats input in cp into gp
 */
format.pieces = function pieces(num) {
    num = parseInt(format.number(num, 0, false), 10);

    var cp = num - (parseInt(num / 10, 10) * 10);
    var sp = parseInt(num / 10, 10) - (parseInt(num / 100, 10) * 10);
    var gp = parseInt(num / 100, 10);

    if (gp === 0 && sp === 0 && cp === 0) {
        return '0 gp';
    }
    text = (gp > 0 ? format.number(gp, 0, true) + '<small>gp</small>, ' : '') +
        (sp > 0 ? sp + '<small>sp</small>, ' : '') +
        (cp > 0 ? cp + '<small>cp</small>, ' : '');
    return text.substr(0, text.length - 2);
};


//-------------------
//----- Helpers -----
//-------------------

/**
 * Returns the suffix for an element's class
 */
format.cstrs = function cstrs(elem, prefix, def) {
    var classes = elem.attr('class');

    var regexp = new RegExp(prefix + '([^ ]*)');
    suffix = classes.match(regexp);
    suffix = (suffix ? suffix[1] : def);

    return suffix;
};

/* returns a numbered suffix for of a class
 * e.g. precise-1 -> 1
 */
format.cnums = function cnums(elem, prefix, def) {
    var num = parseInt(format.cstrs(elem, prefix, def), 10);
    if (isNaN(num)) {
        return 0;
    } else {
        return num;
    }
};

