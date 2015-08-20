(function() {

    var addStockModal = function () {
        return {
            templateUrl: '/static/js/templates/add-stock.html',
            size: 'lg',
            controller: function ($scope, $modalInstance) {
                $scope.cancel = function () {
                    $modalInstance.dismiss();
                };
                $scope.add = function () {
                    $modalInstance.dismiss();
                };

            }
        }
    };

    angular.module('creepycrawly', ['ui.bootstrap'])
        .controller('StockController', ['$scope', '$modal', '$http', '$rootScope',
            function ($scope, $modal, $http, $rootScope) {
                $scope.openAddStockModal = function () {
                    $modal.open(addStockModal());
                };
            }])



})();