define([
    "dcl/dcl",
    "knockout",
    "./ReviewValue",
    "./StixObjectTLP",
    "kotemplate!root-ind:./templates/root-Indicator.html",
    "kotemplate!list-ind:./templates/list-Indicators.html"
], function (declare, ko, ReviewValue, StixObjectTLP) {
    "use strict";

    var KILL_CHAIN_PHASES = ((!(typeof window === "undefined") && window) || {})["killChainPhases"] || {};

    return declare(StixObjectTLP, {
        constructor: function (data, stixPackage) {
            this.producer = ko.computed(function () {
                return stixPackage.safeValueGet(this.id(), this.data(), "producer.identity.name");
            }, this);
            this.confidence = ko.computed(function () {
                return stixPackage.safeValueGet(this.id(), this.data(), "confidence.value.value");
            }, this);
            this.indicatorTypes = ko.computed(function () {
                return stixPackage.safeListGet(this.data(), "indicator_types");
            }, this);
            this.killChainPhase = ko.computed(function () {
                var killChainPhase = stixPackage.safeValueGet(this.id(), this.data(), "kill_chain_phases.kill_chain_phases.0.phase_id");
                if (!(killChainPhase.isEmpty())) {
                    // create a new ReviewValue with the name rather than the id
                    var phaseId = killChainPhase.value();
                    if (KILL_CHAIN_PHASES.hasOwnProperty(phaseId)) {
                        killChainPhase = new ReviewValue(
                            KILL_CHAIN_PHASES[phaseId],
                            killChainPhase.state(),
                            killChainPhase.message()
                        );
                    }
                }
                return killChainPhase;
            }, this);
            this.compositeIndicatorComposition = ko.computed(function () {
                return stixPackage.safeValueGet(this.id(), this.data(), "composite_indicator_expression.operator");
            }, this);
            this.compositeIndicators = ko.computed(function () {
                return stixPackage.safeReferenceArrayGet(this.data(), "composite_indicator_expression.indicators", "idref");
            }, this);
            this.observable = ko.computed(function () {
                var id = stixPackage.safeGet(this.data(), "observable.idref");
                return id ? stixPackage.findByStringId(id) : null;
            }, this);
            this.composition = ko.computed(function () {
                var observable = this.observable();
                return observable ? stixPackage.safeValueGet(this.id(), observable.data(), "observable_composition.operator") : null;
            }, this);
            this.observables = ko.computed(function () {
                var observable = this.observable();
                var observableList = null;
                if (observable) {
                    observableList = stixPackage.safeReferenceArrayGet(observable.data(), "observable_composition.observables", "idref");
                    if (!observableList) {
                        observableList = [observable];
                    }
                }
                return observableList;
            }, this);
            this.relatedIndicators = ko.computed(function () {
                return stixPackage.safeReferenceArrayGet(this.data(), "related_indicators.related_indicators", "indicator.idref");
            }, this);
            this.indicatedTTPs = ko.computed(function () {
                return stixPackage.safeReferenceArrayGet(this.data(), "indicated_ttps", "ttp.idref");
            }, this);
            this.suggestedCOAs = ko.computed(function () {
                return stixPackage.safeReferenceArrayGet(this.data(), "suggested_coas.suggested_coas", "course_of_action.idref");
            }, this);
        }
    });
});
