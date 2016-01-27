/**
 * Created by crespowang on 24/08/2015.
 */
'use strict';

app.controller('HomeCtrl', function ($scope, $log, $filter, MatchFactory,MeFactory) {

    $log.debug('Home Ctrl');
    $scope.match = {};

    MeFactory.getStat().success(function(data){
        $scope.stat = data;
    });


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

