/**
 * Created by crespowang on 24/08/2015.
 */
'use strict';

app.controller('NewMatchCtrl', function ($scope, $log,$filter, $state, MatchFactory) {

    $log.debug('New Match Ctrl');
    $scope.match = {};
    $scope.today = new Date();
    $scope.beforeRender = function($dates){
            var minDate = new Date();
            var maxDate = new Date(minDate.getTime() + 60*60*1000*24*30);
            angular.forEach($dates, function(date) {
                var localDateValue = date.localDateValue();
                date.selectable = localDateValue >= minDate && localDateValue <= maxDate;
            });
    }
    $scope.onTimeSet = function(newTime, oldTime){
        var endTimeInput = new Date(newTime.getTime());
        endTimeInput.setTime(endTimeInput.getTime() + 2*60*60*1000);
        $scope.match.finishTime  = endTimeInput;

        var echeckinTimeInput = new Date(newTime.getTime());
        echeckinTimeInput.setTime(echeckinTimeInput.getTime() - 60 * 1000 * 30);
        $scope.match.checkinEarliest  = echeckinTimeInput;

        var lcheckinTimeInput = new Date(newTime.getTime());
        lcheckinTimeInput.setTime(lcheckinTimeInput.getTime() - 60 * 1000 * 5);
        $scope.match.checkinLatest  = lcheckinTimeInput;


    };

    $scope.createMatch = function(){
        $log.debug("creating the match");
        MatchFactory.createMatch($scope.match).success(function(data){
            $state.go('match', {matchId: data.match.id});

        });
    };

  });

