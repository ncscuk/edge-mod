require([
    "knockout",
    "common/modal/show-error-modal",
    "catalog/cert-catalog-view-model",
    "domReady!"
], function (ko, showErrorModal, SelectModel) {

    var viewModel = new SelectModel(window["rootId"], window["stixPackage"], window["trustGroups"], window["validationInfo"], window["viewURL"], window["editURL"]);

    viewModel.loadStatic({
        "revisions": window["revisions"],
        "rootId": window["rootId"],
        "revision": window["revision"],
        "ajax_uri": window["ajax_uri"],
        "backLinks": window["backLinks"],
        "edges": window["edges"],
        "canPurge": window["canPurge"],
        "canRevoke": window["canRevoke"],
        "sightings": window["sightings"],
        "version": window["version"]
    });

    ko.applyBindings(viewModel);


});