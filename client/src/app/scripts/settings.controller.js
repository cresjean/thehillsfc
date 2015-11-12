/**
 * Created by crespowang on 21/10/2015.
 */
'use strict';
app
    .controller('SettingsCtrl', function ($scope, $log, $state, $rootScope, me, SettingsFactory){

        $log.debug("Settings Ctrl");
        $scope.me = me.data;
         $scope.positions = [
            {name:'GK', id:'GK'},
            {name:'CB', id:'CB'},
            {name:'RB', id:'RB'},
            {name:'LB', id:'LB'},
            {name:'LWB', id:'LWB'},
            {name:'RWB', id:'RWB'},
            {name:'DM', id:'DM'},
            {name:'CM', id:'CM'},
            {name:'AM', id:'AM'},
            {name:'CF', id:'CF'},
            {name:'Coach', id:'Coach'}

        ];
        $scope.me.position = {name: $scope.me.position, id: $scope.me.position};
        $scope.updateMe = function(){

            SettingsFactory.updateMe({name: $scope.me.name, password: $scope.me.password, position: $scope.me.position.id}).success(function(data){
                $rootScope.storage.currentUser.position = $scope.me.position.id;
                $state.go('home');
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