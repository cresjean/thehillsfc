/**
 * Created by crespowang on 9/09/2015.
 */

'use strict';

app.controller('LoginCtrl', function ($scope, $log, $state, LoginFactory){
    $log.debug('Login Ctrl');
    $scope.go_login = function(){

        var username = $scope.username;
        var password = $scope.password;

        $log.debug("Login %s %s", username, password);
        LoginFactory.verifyLogin({'username':username, 'password':password}).success(function(data){
            $state.go('home');
        });


    };
})
    .factory('LoginFactory', function ($http){
      return {
            verifyLogin: function(login){
                return $http.post('/api/people/login', login);
            }
      }
    });