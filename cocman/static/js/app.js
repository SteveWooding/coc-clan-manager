/**
 * Main AngularJS file for the CoC Clan Manager front end application.
 */
(function() {

  var app = angular.module('clanMan', []);

  app.controller('ClanController', ['$scope', '$http', function($scope, $http) {
    // Define an empty object to store the clan data.
    $scope.clanData = {};

    // Define date variables for calculating daily active users.
    $scope.numDailyUsers = 0;
    var timeNow = new Date();
    var oneDayMs = 86400000;
    var timeOneDayAgo = timeNow - oneDayMs;

    // Get the default clan data
    $scope.update = function() {
      $http.get('/api/clandata/mainclan/JSON/')
        .then(function(response) {
          $scope.clanData = response.data;

          // Calculate the total number of wars (used for war win rate, etc)
          $scope.clanData.totalNumWars = ($scope.clanData.warWins +
            $scope.clanData.warTies + $scope.clanData.warLosses);

          // Calculate the number of active users in the past 24 hours
          $scope.clanData.memberList.forEach(function(member) {
            if (Date.parse(member.lastActiveTime) > timeOneDayAgo) {
              $scope.numDailyUsers++;
            }
          });

        }, function(response) {
          $scope.errorMsg = response.statusText + ': ' + response.data.error;
        });
    };

    // Run the update function on the first load of the controller.
    $scope.update();

    // Allow users to sort (forwards and backwards) on column headings.
    $scope.orderCol = 'clanRank';
    $scope.reverse = false;
    $scope.order = function(orderCol) {
      $scope.reverse = ($scope.orderCol === orderCol) ? !$scope.reverse : false;
      $scope.orderCol = orderCol;
    };

  }]);


  // Directive to handle Bootstrap tooltips within AngularJS
  app.directive('bsTooltip', function() {
    return {
      restrict: 'A',
      link: function(scope, element, attrs) {
        $(element).hover(function() {
          // on mouseenter
          $(element).tooltip('show');
        }, function() {
          // on mouseleave
          $(element).tooltip('hide');
        });
      }
    };
  });


})();
