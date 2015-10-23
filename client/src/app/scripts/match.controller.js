/**
 * Created by crespowang on 27/08/2015.
 */
'use strict';

app
    .controller('MatchCtrl', function ($scope, $log, MatchFactory, $stateParams, match, isIn, players,$state, $rootScope) {
    $log.debug("Match Ctrl");
    $scope.match = match.data.match;
    $scope.alreadyIn = isIn.data.in;
    $scope.leave = false;
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
        if (player.id == $rootScope.storage.currentUser.id){
            $scope.leave = player.leave;
        }
        $scope.players.push(player);
    });

    $scope.teams = teams;

    $scope.$watchCollection('teams', function(newVal, oldVal){
        angular.forEach(newVal, function(v, k){
            if (oldVal[k] != v){
                MatchFactory.teamUp(k,v).success(function(data){

                });

            }
        });

    });


    $scope.askLeave = function(){
        $log.debug("ask leave");
        MatchFactory.askLeave( $scope.match.id, !$scope.leave).then(function(){
            $log.debug("leave");

            $scope.leave = !$scope.leave;
            var not_existing = true;
            angular.forEach($scope.players, function(player){
                if (player.id == $rootScope.storage.currentUser.id){
                    player.leave = $scope.leave ;
                    not_existing = false;
                }
            });
            if (not_existing){
                $log.debug("reload");
                $state.reload();
            }

        });
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
            },
            askLeave: function(match_id, status){
                return $http.post('/api/matches/'+match_id+'/leave', {status:status});
            }
      }
    })
;