/**
 * Created by crespowang on 24/08/2015.
 */
'use strict';

app.controller('HomeCtrl', function ($scope, $log,$filter, MatchFactory) {

    $log.debug('Home Ctrl');
    $scope.match = {};
    $log.debug('Welcome ' + $scope.storage.currentUser.name);
    MatchFactory.getAllMatches().success(function(data){
            $log.debug("Fetching all matches");
            $scope.matches =  data['matches'];
        }
    );
  }).
factory('MatchFactory', function ($http){
      return {
            getAllMatches: function(){
                return $http.get('/api/matches');
            },
            createMatch: function(match){
                return $http.post('/api/matches', match);
            },
            getMatch: function(match_id){
                return $http.get('/api/matches/'+match_id);
            }
      }
    });

