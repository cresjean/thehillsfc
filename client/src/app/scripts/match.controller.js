/**
 * Created by crespowang on 27/08/2015.
 */
'use strict';

app.controller('MatchCtrl', function ($scope, $log, MatchFactory, match) {
    $log.debug("Match Ctrl");
    $scope.match = match.data.match;

})
;