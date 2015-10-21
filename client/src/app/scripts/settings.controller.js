/**
 * Created by crespowang on 21/10/2015.
 */
'use strict';
app
    .controller('SettingsCtrl', function ($scope, $log, $state, $rootScope, me, SettingsFactory){

        $log.debug("Settings Ctrl");
        $scope.me = me.data;
        $scope.updateMe = function(){
            $log.debug("update me");
            SettingsFactory.updateMe({"name": $scope.me.name, "password": $scope.me.password}).success(function(data){
                $state.go('settings');
            });

        }


})
    .factory('SettingsFactory', function ($http){
        return {
            getMe: function(){
                return $http.get('/api/people/me');
            },
            updateMe: function(newme){
                return $http.post('/api/people/me', newme);
            }
        }
    });