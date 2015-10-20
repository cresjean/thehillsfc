/**
 * Created by crespowang on 27/08/2015.
 */
'use strict';

app
    .controller('MatchCtrl', function ($scope, $log, MatchFactory, $stateParams, match, isIn) {
    $log.debug("Match Ctrl");
    $scope.match = match.data.match;
    $scope.alreadyIn = isIn.data.in;
    MatchFactory.getPlayers($stateParams.matchId).success(function(data){
        $scope.players = data.people;
    });
    $scope.signup_match = function(){
        $log.debug("signup");
    };

})
    .controller('SignInMatchCtrl', function($scope, $log, MatchFactory, match) {
        $scope.match = match.data.match;



})
    .controller('SignUpMatchCtrl', function($scope, $log, MatchFactory, match) {
        $scope.match = match.data.match;

})
    .factory('MatchFactory', function ($http){
      return {
            getAllMatches: function(){
                return $http.get('/api/matches');
            },
            createMatch: function(match){
                return $http.post('/api/matches', match);
            },
            getMatch: function(match_id){
                return $http.get('/api/matches/'+match_id);
            },
            getPlayers: function(match_id){
                return $http.get('/api/matches/'+match_id+'/registered-people');
            },
            getPlayer: function(match_id, people_id){
                return $http.get('/api/matches/'+match_id+'/'+people_id);
            },
            signUp: function(match_id, match_code) {
                return $http.post('/api/matches/'+match_id+'/signmeup', {code:match_code});
            }
      }
    })
;