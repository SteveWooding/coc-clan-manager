/**
 * Main AngularJS file for the CoC Clan Manager front end application.
 */
(function() {

  var app = angular.module('clanMan', []);

  app.controller('ClanController', ['$scope', '$http', function($scope, $http) {
    $scope.clanData = {};

    // Get the default clan data
    $http.get('/clandata/mainclan/JSON/')
      .success(function(data) {
        if (data.status === 200) {
          $scope.clanData = data.clanData;
        }
        else {
          $scope.errorMsg = data.error;
        }
      })
      .error(function () {
        $scope.errorMsg = 'Whoops! Internal Server. Sorry. ¯\\_(ツ)_/¯';
      });

    // Allow users to sort (forwards and backwards) on column headings.
    $scope.orderCol = 'clanRank';
    $scope.reverse = false;
    $scope.order = function(orderCol) {
      $scope.reverse = ($scope.orderCol === orderCol) ? !$scope.reverse : false;
      $scope.orderCol = orderCol;
    };

    // Convert league ID into the corresponding shield image
    // TODO: May have to store this data in the database in case of change and
    // to be more flexible. Just storing the common leagues here, not all of
    // them.
    $scope.getShieldImg = function(leagueId) {
      var shieldImages = {
        29000000: "https://api-assets.clashofclans.com/leagues/36/e--YMyIexEQQhE4imLoJcwhYn6Uy8KqlgyY3_kFV6t4.png",
        29000003: "https://api-assets.clashofclans.com/leagues/36/SZIXZHZxfHTmgseKCH6T5hvMQ3JQM-Js2QfpC9A3ya0.png",
        29000004: "https://api-assets.clashofclans.com/leagues/36/QcFBfoArnafaXCnB5OfI7vESpQEBuvWtzOyLq8gJzVc.png",
        29000005: "https://api-assets.clashofclans.com/leagues/36/8OhXcwDJkenBH2kPH73eXftFOpHHRF-b32n0yrTqC44.png",
        29000006: "https://api-assets.clashofclans.com/leagues/36/nvrBLvCK10elRHmD1g9w5UU1flDRMhYAojMB2UbYfPs.png",
        29000007: "https://api-assets.clashofclans.com/leagues/36/vd4Lhz5b2I1P0cLH25B6q63JN3Wt1j2NTMhOYpMPQ4M.png",
        29000008: "https://api-assets.clashofclans.com/leagues/36/Y6CveuHmPM_oiOic2Yet0rYL9AFRYW0WA0u2e44-YbM.png",
        29000009: "https://api-assets.clashofclans.com/leagues/36/CorhMY9ZmQvqXTZ4VYVuUgPNGSHsO0cEXEL5WYRmB2Y.png",
        29000010: "https://api-assets.clashofclans.com/leagues/36/Hyqco7bHh0Q81xB8mSF_ZhjKnKcTmJ9QEq9QGlsxiKE.png",
        29000011: "https://api-assets.clashofclans.com/leagues/36/jhP36EhAA9n1ADafdQtCP-ztEAQjoRpY7cT8sU7SW8A.png",
        29000012: "https://api-assets.clashofclans.com/leagues/36/kSfTyNNVSvogX3dMvpFUTt72VW74w6vEsEFuuOV4osQ.png",
        29000013: "https://api-assets.clashofclans.com/leagues/36/pSXfKvBKSgtvfOY3xKkgFaRQi0WcE28s3X35ywbIluY.png",
        29000015: "https://api-assets.clashofclans.com/leagues/36/olUfFb1wscIH8hqECAdWbdB6jPm9R8zzEyHIzyBgRXc.png",
        29000014: "https://api-assets.clashofclans.com/leagues/36/4wtS1stWZQ-1VJ5HaCuDPfdhTWjeZs_jPar_YPzK6Lg.png",
        29000016: "https://api-assets.clashofclans.com/leagues/36/JmmTbspV86xBigM7OP5_SjsEDPuE7oXjZC9aOy8xO3s.png"
      };

      return shieldImages[leagueId];
    };

  }]);


})();