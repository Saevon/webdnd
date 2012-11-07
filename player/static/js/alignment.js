alignment = {
    moral: 50,
    order: 50,
    ratio: 2,

    elem: function(elem) {
        this.elem = elem;
        this.pointer = elem.find('.align-pointer');
        return this;
    },
    update: function(order, moral) {
        this.order = order;
        this.moral = moral;
        this.refresh();
    },
    refresh: function() {
        this.elem.find('.align-moral')
            .val(this.moral);
        this.elem.find('.align-order')
            .val(this.order);
        var text = this.text();
        this.elem.find('.align-text')
            .val(text);

        this.pointer.css('top', (this.moral * this.ratio) - (this.pointer.width() / 2) + 'px');
        this.pointer.css('left', (this.order * this.ratio) - (this.pointer.height() / 2) + 'px');
    },
    text: function() {
        var pre, suf;
        if (this.order >= 70) {
            pre = 'Lawful';
        } else if (this.order <= 30) {
            pre = 'Chaotic';
        } else {
            pre = 'True';
        }
        if (this.moral >= 70) {
            suf = 'Good';
        } else if (this.moral <= 30) {
            suf ='Evil';
        } else {
            suf = pre == 'True' ? 'Neutral' : pre;
            pre = 'True';
        }
        return pre + ' ' + suf;
    },
    read: function(string) {
        string = string.toLowerCase();
        moral = 50;
        order = 50;

        if ('chaotic' in string) {
            order = 30;
        } else if ('lawful' in string) {
            order = 70;
        }

        if ('good' in string) {
            moral = 30;
        } else if ('evil' in string) {
            moral = 70;
        }

        return {
            moral: moral,
            order: order
        };
    },
    events: function() {
        var _this = this;
        this.elem.find('.align-moral').on('change', function() {
            _this.update(_this.order, $(this).val());
        });
        this.elem.find('.align-order').on('change', function() {
            _this.update($(this).val(), _this.moral);
        });
        this.elem.find('.align-text').on('change', function() {
            var align = _this.read($(this).val());
            _this.update(align.order, align.moral);
        });

        var move = function(elem, e) {
            var offset = elem.offset(); 
            //or $(this).offset(); if you really just want the current element's offset
            var x = e.pageX - offset.left - 5;
            var y = e.pageY - offset.top - 5;

            if (x < 0) {
                x = 0;
            } else if (x >= 200) {
                x = 200;
            }
            if (y < 0) {
                y = 0;
            } else if (y >= 200) {
                y = 200;
            }

            _this.update(Math.round(x / 2), Math.round(y / 2));
        };

        var clicked = false;
        this.elem.find('.align-select-box').on('mousedown', function(e) {
            clicked = true;
            var elem = $(this);
            move(elem, e);
        });
        $(document).on('mouseup', function() {
            clicked = false;
        });
        this.elem.find('.align-select-box').on('mousemove', function(e) {
            if (!clicked) {
                return;
            }
            var elem = $(this);
            move(elem, e);
        });
    }
};
