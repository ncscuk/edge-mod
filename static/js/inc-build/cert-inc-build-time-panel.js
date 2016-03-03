define([
    "dcl/dcl",
    "knockout",
    "common/cert-abstract-builder-form",
    "inc-build/cert-inc-build-time"
], function (declare, ko, AbstractBuilderForm, Time) {
    "use strict";

    return declare(AbstractBuilderForm, {
        declaredClass: "TimePanel",

        constructor: declare.superCall(function (sup) {
            return function () {
                this.timeTypes = ko.observableArray();
                sup.call(this, "Times");
            }
        }),

        counter: function () {
            var count = 0;
            ko.utils.arrayForEach(this.timeTypes(), function (timeType) {
                if (timeType.timeString() != "") {
                    count++;
                }
            });
            return count != 0 ? count : "";
        },

        loadStatic: function (optionsList) {
            this.timeTypes.removeAll();
            for (var i = 0; i < optionsList['time_types_list'].length; i++) {

                var name = optionsList['time_types_list'][i][0]
                var displayName = optionsList['time_types_list'][i][1]
                var required = optionsList['time_types_list'][i][2]

                var newTime = new Time(
                        name,
                        displayName
                        )

                newTime.timeString.extend({
                            requiredGrouped: {
                                required: required,
                                group: this.validationGroup,
                                displayMessage: displayName + " time is required for your indicator"
                            }
                        })

                this.timeTypes.push(newTime);
            }
        },

        load: function (data) {
            var self = this;
            ko.utils.arrayForEach(self.timeTypes(), function (timeType) {
                timeType.load("");
            });


            if ('time' in data) {
                $.each(data['time'], function (i, v) {
                    ko.utils.arrayForEach(self.timeTypes(), function (timeType) {
                        if (timeType.saveName() === i) {
                            timeType.load(v);
                        }
                    });
                });
            }
        },

        save: function () {
            var dataTime = {};
            ko.utils.arrayForEach(this.timeTypes(), function (item) {
                if (item.timeString() != "") {
                    dataTime[item.saveName()] = {
                        'value': item.timeString(),
                        'precision': 'second' //Hardcoded for now and strictly not needed for 'second'.
                    };
                }
            });

            var data = {};
            data['time'] = dataTime
            return data;
        }
    })
});




