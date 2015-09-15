/**
 * Created by crespowang on 15/09/2015.
 */

'use strict';

app.controller('CheckinMatchCtrl', function ($scope, $log,$filter, $state, match) {
    $scope.match = match.data.match;

});
