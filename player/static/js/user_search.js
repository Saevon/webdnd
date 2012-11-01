

var friends = {};

friends.unique = (function() {
    var users = {};

    var unique = function unique(elem, add) {
        var id = elem;
        if (typeof(elem) != 'number') {
            id = elem.data('id');
        }

        if (users[id] !== undefined) {
            return false;
        } else {
            if (add) {
                users[id] = true;
            }
            return true;
        }
    };

    return unique;
})();

friends.user = (function() {

    var add = function(elem) {
        var type = elem.data('type');
        friends.unique(elem, true);
        if (type == 'search-user') {
            elem.detach().appendTo('#input-friends');
            elem.find('input').attr('name', 'new-friends[]');

            elem.removeClass('search-user');
            elem.addClass('new-friend');
            elem.data('type', 'new-friend');

            $('#input-friends').find('.empty').hide();
        } else if (type == 'unfriend') {
            elem.find('input').attr('name', 'friends[]');

            elem.removeClass('unfriend');
            elem.addClass('friend');
            elem.data('type', 'friend');
        }
    };

    var remove = function(elem) {
        var type = elem.data('type');
        if (type == 'friend') {
            elem.find('input').attr('name', 'unfriends[]');

            elem.removeClass('friend');
            elem.addClass('unfriend');
            elem.data('type', 'unfriend');
        } else if (type == 'new-friend') {
            elem.remove();
            var input = $('#input-friends');
            if (input.find('.unfriend')
                    .add(input.find('.friend'))
                    .add(input.find('.new-friend')).length === 0
            ) {
                $('#input-friends').find('.empty').show();
            }
        }
    };

    var events = function(elem) {
        elem.on('click', '.action.remove', function() {
            remove(elem);
        });
        elem.on('click', '.action.add', function(e, item) {
            add(elem);
        });
    };

    var user = function(elem) {
        events(elem);
    };
    return user;
})();

friends.search = (function() {
    var result  = {
        endpoint: '/api/account/search/',
        template: 'users',
        template_empty: 'search-user-empty',
        _request: false,

        elem: function(elem) {
            this._elem = elem;
            return this;
        },

        clear: function() {
            this._elem.empty();
            this._elem.append(
                Templates[this.template_empty]({})
            );
        },

        render: function(response) {
            this._elem.empty();

            if (!response.paging.length) {
                this._elem.append(
                    Templates[this.template_empty](response.output)
                );
            } else {
                var data = {'players': response.output};
                var length = data.players.length;
                for (var i=0; i < length; i++) {
                    data.players[i].type = "search-user";
                }

                this._elem.append(
                    Templates[this.template](data)
                );

                var kept = 0;
                this._elem.find('.user').each(function() {
                    var elem = $(this);
                    if (friends.unique(elem)) {
                        friends.user(elem);
                        kept++;
                    } else {
                        elem.remove();
                    }
                });
                if (!kept) {
                    this._elem.append(
                        Templates[this.template_empty](response.output)
                    );
                }
            }
        },

        request: function(val) {
            if (this._request !== false) {
                this._request.abort();
            }

            var _this = this;
            this._request = $.ajax(this.endpoint + val, {
                dataType: 'json',
                success: function(response) {
                    _this.render(response);
                },
                error: function(response) {
                    if (response.statusText != 'abort') {
                        console.error(response);
                    }
                }
            });
        }
    };

    var search = function(input, output) {
        var obj = $.extend({}, result).elem(output);
        obj.refresh = function() {
            var val = input.val();
            obj.request(val);
        };

        input.on('change', function() {
            obj.refresh();
        });
        input.keyup(function(e) {
            var key = e.keyCode || window.event.keyCode;

            // Enter
            if (key == 13) {
                obj.refresh();
                e.preventDefault();
            // Backspace, Delete, Space, A-Z
            } else if (key == 8 || key == 46 || key == 32
                    || (key >= 65 && key <= 90)
            ) {
                obj.refresh();
            }
        });
        input.keypress(function(e) {
            var key = e.keyCode || window.event.keyCode;
            // Enter
            if (key == 13) {
                e.preventDefault();
            }
        });

        return obj;
    };
    return search;
})();
