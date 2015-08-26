/**
 * Created by crespowang on 24/08/2015.
 */
'use strict';

app.controller('HomeCtrl', function ($scope, $log,$filter, MatchFactory) {
    $log.debug('Home Ctrl');
    $scope.match = {};
    $scope.today = new Date();
    $scope.onTimeSet = function(newTime, oldTime){
        var endTimeInput = new Date(newTime.getTime());
        endTimeInput.setTime(endTimeInput.getTime() + 2*60*60*1000);
        $scope.match.finishTime  = endTimeInput;

        var echeckinTimeInput = new Date(newTime.getTime());
        echeckinTimeInput.setTime(echeckinTimeInput.getTime() - 60*60*1000);
        $scope.match.checkinEarliest  = echeckinTimeInput;

        var lcheckinTimeInput = new Date(newTime.getTime());
        lcheckinTimeInput.setTime(lcheckinTimeInput.getTime() - 60 * 1000 * 5);
        $scope.match.checkinLatest  = lcheckinTimeInput;

    };

    $scope.createMatch = function(){
        $log.debug("creating the match");
        MatchFactory.createMatch($scope.match).success(function(data){
            $scope.matches.push(data['match']);
        });
    };
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
            }
      }
    });

