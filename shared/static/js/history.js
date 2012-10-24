// History Log
// Stores typed values so you can find
// them again later
History = function() {
    var lines = [];
    var hist_index = 0;
    var limit = -1;

    var history = {
        /**
         * Change history list to the given list
         */
        store: function(arr) {
            lines = [];
            lines[-1] = '';
            for (var key in arr) {
                this.add(key);
            }
            return this;
        },
        
        /**
         * Adds a single entry to the history
         */
        add: function(cmd) {
            if (limit <= 0 || lines.length < limit) {
                lines.push(cmd);
                hist_index = -1;
                return this;
            }
        },

        /**
         * Returns the current item
         */
        get: function() {
            return lines[hist_index] || '';
        },

        /**
         * Returns the next item in the index
         */
        next: function() {
            this.set_index(hist_index + 1);
            return this.get();
        },
        /**
         * Returns the prev item in the index
         */
        prev: function() {
            this.set_index(hist_index - 1);
            return this.get();
        },
        /**
         * Resets the index
         */
        reset: function() {
            hist_index = -1;
            return this;
        },

        /**
         * Sets the index to the given value
         */
        set_index: function(val) {
            this._set_index(val);
        },
        /**
         * Sets the index to the given value after performing some
         * validation
         */
        _set_index: function(val) {
            if (val >= lines.length) {
                hist_index = -1;
            } else if (val < -1) {
                hist_index = lines.length - 1;
            } else {
                hist_index = val;
            }
        }
    };
    return history;
};
