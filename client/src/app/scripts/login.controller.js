/**
 * Created by crespowang on 9/09/2015.
 */

'use strict';

app.controller('LoginCtrl', function ($scope, $log, $state, LoginFactory){
    $log.debug('Login Ctrl');
    $scope.LoginFactory = LoginFactory;
    $scope.LoginFactory.setLoginStatus(false);
    $scope.go_login = function(){

        var username = $scope.username;
        var password = $scope.password;

        LoginFactory.verifyLogin({'username':username, 'password':password}).success(function(data){
            $scope.LoginFactory.setLoginStatus(true);
            $log.debug($scope.LoginFactory.getLoginStatus());
            $state.go("home");
        });


    };
})

    .factory('LoginFactory', function ($http){
        var loginStatus = true;
        var user;

        return {
            verifyLogin: function(login){
                return $http.post('/api/people/login', login);
            },
            logout: function(){
                return $http.get('/logout');
            },
            getLoginStatus: function () {
                return loginStatus;
            },
            setLoginStatus: function(login_status) {
                loginStatus = login_status;
            },
            setUser: function(userInfo) {
                user = userInfo;
            },
            getUser: function() {
                return user;
            }
        }
    });