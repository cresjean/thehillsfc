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
  })
;

