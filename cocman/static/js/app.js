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

  }]);


})();