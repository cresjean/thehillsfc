/**
 * Created by crespowang on 27/08/2015.
 */
'use strict';

app
  .filter('ontime', function(){
    return function(players){
      var ontime = []
      for (var i = 0; i < players.length; i++){
        var player = players[i];
        if (player.signinOntime && !player.signupMissing){
          ontime.push(player);
        }
      }
      return ontime;

    }
  })
  .filter('late', function(){
    return function(players){
      var late = [];
      for (var i = 0; i < players.length; i++){
        var player = players[i];
        if (player.signinOntime && !player.signupMissing){

        }
        else{
          late.push(player);
        }
      }
      return late;
    }
  })
  .controller('MatchCtrl', function($scope, $log, MatchFactory, $stateParams, match, isIn, players, $state, $rootScope) {
    $log.debug("Match Ctrl");
    $scope.match = match.data.match;
    $scope.alreadyIn = isIn.data.in;
    $scope.leave = false;
    $scope.players = [];
    var now = new Date();
    var latestSignup = new Date($scope.match.startTime * 1000);
    var deadline = new Date($scope.match.startTime * 1000);
    deadline.setHours(deadline.getHours() + 2);

    latestSignup.setHours(latestSignup.getHours() - 6);
    $log.debug(latestSignup);
    $log.debug(deadline);


    $scope.signupOpen = true;
    if (now > latestSignup) {
      $scope.signupOpen = false;
    }

    if (now > deadline)
    {
      $log.debug("Dead");
      $scope.deadline = true;
    }

    var teams = {};

    angular.forEach(players.data.people, function(player) {

      if (player.team == null) {
        teams[player.playId] = undefined;
      } else {
        teams[player.playId] = player.team;
      }
      if (player.id == $rootScope.storage.currentUser.id) {
        $scope.leave = player.leave;
      }
      $scope.players.push(player);
    });

    $scope.teams = teams;

    $scope.$watchCollection('teams', function(newVal, oldVal) {
      angular.forEach(newVal, function(v, k) {
        if (oldVal[k] != v) {
          MatchFactory.teamUp(k, v).success(function(data) {

          });

        }
      });

    });

    $scope.manualCheckin = function(playerId) {
      $log.debug("manual check in " + playerId);
      MatchFactory.manualCheckin(playerId, $scope.match.id).then(function() {
        angular.forEach($scope.players, function(player) {
          if (player.id == playerId) {
            player.signinOntime = true;
            player.signinTime = new Date();
          }
        });
      });

    };


    $scope.manualFine = function(player, dollar) {
      var playerId = player.id;

      $log.debug("manual fine " + playerId);
      MatchFactory.manualFine(playerId, $scope.match.id, dollar).then(function() {
        player.finePaid = dollar;

      });

    }

    $scope.cancelMatch = function() {
      MatchFactory.cancelMatch($scope.match.id).then(function() {
        $state.go('home');

      });
    };

    $scope.submitComment = function() {
      MatchFactory.submitComment($scope.match.id, $scope.match.comment).then(function() {

      });
    }

    $scope.openMatch = function() {
      MatchFactory.openMatch($scope.match.id).then(function() {
        $state.go('home');

      });
    };

    $scope.askLeave = function() {
      $log.debug("ask leave");
      MatchFactory.askLeave($scope.match.id, !$scope.leave).then(function() {
        $log.debug("leave");

        $scope.leave = !$scope.leave;
        var not_existing = true;
        angular.forEach($scope.players, function(player) {
          if (player.id == $rootScope.storage.currentUser.id) {
            player.leave = $scope.leave;
            not_existing = false;
          }
        });
        if (not_existing) {
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
  .factory('MatchFactory', function($http) {
    return {
      getAllMatches: function() {
        return $http.get('/api/matches');
      },
      createMatch: function(match) {
        return $http.post('/api/matches', match);
      },
      getMatch: function(match_id) {
        return $http.get('/api/matches/' + match_id);
      },
      getPlayers: function(match_id) {
        return $http.get('/api/matches/' + match_id + '/registered-people');
      },
      getPlayer: function(match_id, people_id) {
        return $http.get('/api/matches/' + match_id + '/' + people_id);
      },
      signUp: function(match_id, match_code) {
        return $http.post('/api/matches/' + match_id + '/signmeup', {
          code: match_code
        });
      },
      teamUp: function(play_id, team) {
        return $http.post('/api/play/' + play_id + '/teamup', {
          team: team
        });
      },
      askLeave: function(match_id, status) {
        return $http.post('/api/matches/' + match_id + '/leave', {
          status: status
        });
      },
      cancelMatch: function(match_id) {
        return $http.post('/api/matches/' + match_id + '/status/cancel');
      },
      openMatch: function(match_id) {
        return $http.post('/api/matches/' + match_id + '/status/open');
      },
      manualCheckin: function(people_id, match_id) {
        return $http.post('/api/matches/' + match_id + '/manualsignin/' + people_id);
      },
      manualFine: function(people_id, match_id, dollar) {
        return $http.post('/api/matches/' + match_id + '/manualfine/' + people_id, {
          dollar: dollar
        });
      },
      submitComment: function(match_id, comment) {
        return $http.post('/api/matches/' + match_id + '/comment', {
          comment: comment
        });


      }
    }
  });
