/**
 * Main AngularJS file for the CoC Clan Manager front end application.
 */
(function() {

  var app = angular.module('clanMan', []);

  app.controller('ClanController', ['$scope', '$http', function($scope, $http) {
    $scope.clanData = {};

    // Get the default clan data
    $http.get('/clandata/mainclan/JSON/').success(function(data) {
      if (data.status === 200) {
        $scope.clanData = data.clanData;
      }
      else {
        $scope.errorMsg = data.error;
      }
    });

    // Allow users to sort (forwards and backwards) on column headings.
    $scope.orderCol = 'clanRank';
    $scope.reverse = false;
    $scope.order = function(orderCol) {
      $scope.reverse = ($scope.orderCol === orderCol) ? !$scope.reverse : false;
      $scope.orderCol = orderCol;
    };

  }]);


})();