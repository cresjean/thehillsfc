/**
 * Created by crespowang on 9/09/2015.
 */

'use strict';

app.controller('LoginCtrl', function ($scope, $log, $state, $rootScope, LoginFactory, $localStorage){
    $log.debug('Login Ctrl');
    $scope.login = {};
    $scope.LoginFactory = LoginFactory;
    $scope.LoginFactory.setLoginStatus(false);
    $scope.go_login = function(){

        var username = $scope.username;
        var password = $scope.password;
        $scope.login = {};
        $scope.login.checking = true;
        LoginFactory.verifyLogin({'username':username, 'password':password}).then(function(data){
            $scope.login.checking = false;
            $scope.login.success = true;
            $scope.login.message = "All good! Redirecting ...";
            $scope.LoginFactory.setLoginStatus(true);
            $rootScope.storage = $localStorage;
            $rootScope.storage.currentUser = data.data;

            $state.go("home");
        },
        function(data){
            $scope.login.checking = false;
            $scope.login.error = true;
            $scope.login.message = "Oops something wrong!";
            $log.debug("bad login");

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
    .controller('PasswordResetCtrl', function($scope, $log, $rootScope, $localStorage, LoginFactory, $state){
        $log.debug('PasswordResetCtrl');
        $scope.login = {};
        $scope.reset = function(){
             $scope.login = {};
            LoginFactory.resetPassword($scope.password, $scope.email).then(function () {
                    $scope.login.success = true;
                    $scope.login.message = "Please use your new password to login";

               $state.go('login');
            },
            function(){
                $scope.login.error = true;
                $scope.login.message = "Email does not exist";
            });
        };


    })
    .factory('LoginFactory', function ($http){
        var loginStatus = true;
        var user;

        return {
            resetPassword: function(pwd, email){
                return $http.post('/api/people/password-reset',{password: pwd, email:email});
            },
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