/**
 * Main AngularJS file for the CoC Clan Manager front end application.
 */
(function() {

  var app = angular.module('clanMan', []);

  app.controller('ClanController', ['$scope', '$http', function($scope, $http) {
    $scope.clanData = {};

    // Get the default clan data
    $http.get('/api/clandata/mainclan/JSON/')
      .then(function (response) {
          $scope.clanData = response.data;
      }, function (response) {
        $scope.errorMsg = response.statusText + ': ' + response.data.error;
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