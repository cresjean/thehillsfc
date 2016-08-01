/**
 * Created by crespowang on 24/08/2015.
 */
'use strict';

app.controller('HomeCtrl', function ($scope, $log, $filter, $q, MatchFactory, MeStat) {

    $log.debug('Home Ctrl');
    $scope.match = {};
    $scope.stat = MeStat.data;
    $scope.now = new Date();
    MatchFactory.getAllMatches().success(function(data){
            $log.debug("Fetching all matches");
            $scope.matches =  data['matches'];
        }
    );
  })

.factory('MeFactory', function ($http){
      return {
            getStat: function(){
                return $http.get('/api/people/me/stat');
            }
      }
    })
;
