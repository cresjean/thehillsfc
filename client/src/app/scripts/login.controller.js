/**
 * Created by crespowang on 9/09/2015.
 */

'use strict';

app.controller('LoginCtrl', function ($scope, $log, $state, $rootScope, LoginFactory, $localStorage){
    $log.debug('Login Ctrl');
    $scope.LoginFactory = LoginFactory;
    $scope.LoginFactory.setLoginStatus(false);
    $scope.go_login = function(){

        var username = $scope.username;
        var password = $scope.password;

        LoginFactory.verifyLogin({'username':username, 'password':password}).success(function(data){
            $scope.LoginFactory.setLoginStatus(true);
            $rootScope.storage = $localStorage;
            $rootScope.storage.currentUser = data;
            $state.go("home");
        });


    };
})
    .controller('LogoutCtrl', function($scope, $log, $rootScope, $localStorage, LoginFactory, $state){
        $log.debug('Logout Ctrl');
            $rootScope.storage.currentUser = undefined;
        LoginFactory.logout().success(function(){
            $state.go('login');
        });

    })
    .factory('LoginFactory', function ($http){
        var loginStatus = true;
        var user;

        return {
            isLogin: function(){
                return $http.get('/api/people/login');
            },
            verifyLogin: function(login){
                return $http.post('/api/people/login', login);
            },
            logout: function(){
                return $http.get('/api/people/logout');
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