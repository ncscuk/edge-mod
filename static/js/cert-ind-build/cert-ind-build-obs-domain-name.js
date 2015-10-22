define([
    "dcl/dcl",
    "cert-ind-build/indicator-builder-shim",
    "cert-ind-build/validation"
], function (declare, indicator_builder, validation) {
    "use strict";

    var CERTObservableDomainName = declare(indicator_builder.ObservableDomainName, {
        constructor: function () {
            this.type.extend({
                validate: {
                    "isValidCallback": validation.hasValue,
                    "failedValidationMessage": "A domain type is required."
                }
            }).valueHasMutated(); // Have to force a refresh to trigger validation, in batch mode this field isn't visible so the binding isn't re-evaluated.
        },

        doValidation: declare.superCall(function (sup) {
            return function () {
                var msgs = sup.call(this);
                if (this.type.hasError()) {
                    msgs.addError(this.type.errorMessage());
                }
                return msgs;
            };
        })
    });
    indicator_builder.ObservableDomainName = CERTObservableDomainName;
    return CERTObservableDomainName;
});
