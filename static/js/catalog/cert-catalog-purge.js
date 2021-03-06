define([
    "dcl/dcl",
    "knockout",
    "common/modal/show-publish-modal",
    "common/modal/show-error-modal"
], function (declare, ko, showPublishModal, showErrorModal) {
    "use strict";

    return declare(null, {
        declaredClass: "CatalogPurge",
        constructor: function () {
            this.label = ko.observable("Purge");
            this.canRevoke = ko.observable("");
            this.canPurge = ko.observable("");
            this.ajaxURI = ko.observable("");
            this.stixID = ko.observable("");
        },

        loadStatic: function (optionsList) {
            this.canRevoke(optionsList.canRevoke);
            this.canPurge(optionsList.canPurge);
            this.ajaxURI(optionsList.ajax_uri);
            this.stixID(optionsList.rootId);
        },

        createParams: function () {
            return {
                "id": this.stixID()
            }
        },

        revokeObject: function () {
            postJSON(this.ajaxURI() + "revoke_object/", this.createParams(), function (response) {
                if (response["success"] === true) {
                    showPublishModal("Revoked", "The STIX object has been successfully revoked", false);
                } else {
                    showErrorModal("Couldn't Revoke this Stix Object", false)
                }
            }.bind(this));
        },

        purgeObject: function () {
            postJSON(this.ajaxURI() + "purge_object/", this.createParams(), function (response) {
                if (response["success"] === true) {
                    document.location = '/catalog/' + response['type'] + '/';
                } else {
                    showErrorModal("Couldn't Revoke this Stix Object", false)
                }
            }.bind(this));

        }
    });
});
