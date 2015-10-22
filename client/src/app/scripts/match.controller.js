/**
 * Created by crespowang on 27/08/2015.
 */
'use strict';

app
    .controller('MatchCtrl', function ($scope, $log, MatchFactory, $stateParams, match, isIn, players) {
    $log.debug("Match Ctrl");
    $scope.match = match.data.match;
    $scope.alreadyIn = isIn.data.in;
    //$scope.players = players.data.people;
    //MatchFactory.getPlayers($stateParams.matchId).success(function(data){
    //    $scope.players = data.people;
    //    var teams = {};
    //    angular.forEach($scope.players, function(player){
    //        teams[player.id] = player.team;
    //
    //    });
    //    $scope.teams = teams;
    //
    //});
        $scope.players = [];

        var teams = {};

        angular.forEach(players.data.people, function(player){

            if (player.team == null){
                teams[player.playId] = undefined;
            }
            else
            {
                teams[player.playId] = player.team;

            }
            $scope.players.push(player);
        });

        $scope.teams = teams;

        $scope.$watchCollection('teams', function(newVal, oldVal){
            angular.forEach(newVal, function(v, k){
                if (oldVal[k] != v){
                    $log.debug(k+" changes to "+v);
                    MatchFactory.teamUp(k,v).success(function(data){

                    });

                }
            });

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
            },
            teamUp: function(play_id, team) {
                return $http.post('/api/play/'+play_id+'/teamup', {team: team});
            }
      }
    })
;