webdnd = function() {

};

webdnd.user = (function() {
    var users = [];
    var self;

    var user = function(uid) {
        return users[uid];
    };

    user.update = function(uid, values) {
        if (users[uid] === undefined) {
            users[uid] = {
                uid: uid,
                name: '',
                color: false,
                status: 'online'
            };
        }
        $.extend(users[uid], values);
    };

    user.all = function(include_self) {
        include_self = (include_self === undefined) ? false : include_self;

        var out = $.extend(true, {}, users);
        if (!include_self) {
            users[self] = undefined;
        }
        return out;
    };

    user.self = function(uid) {
        if (uid !== undefined) {
            self = uid;
        }
        return self;
    };

    return user;
})();


