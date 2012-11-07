alignment = {
    moral: 50,
    order: 50,

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

        this.pointer.css('top', (this.moral * this.ratio) + 'px');
        this.pointer.css('left', (this.order * this.ratio) + 'px');
    },
    text: function() {
        var pre, suf;
        if (this.moral >= 70) {
            pre = 'Good';
        } else if (this.moral <= 30) {
            pre ='Evil';
        } else {
            pre = 'True';
        }
        if (this.order >= 70) {
            suf = 'Lawful';
        } else if (this.order <= 30) {
            suf = 'Chaotic';
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
            var laign = _this.read($(this).val());
            _this.update(align.order, align.moral);
        });
        var clicked = false;
        this.find('.align-select-group').on('mousedown', function() {
            clicked = true;
        });
        $(document).on('mouseup', function() {
            clicked = false;
        });
        this.find('.align-select-group').on('mousemove', function(e) {
            console.log(e)
        });
    }
};
