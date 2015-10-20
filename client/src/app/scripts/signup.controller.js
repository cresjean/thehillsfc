/**
 * Created by crespowang on 24/08/2015.
 */
'use strict';

app.controller('SignUpCtrl', function ($scope, $log, $state, $rootScope, $localStorage, SignUpFactory){
    $log.debug("SignUp Ctrl");
    $scope.go_signup = function(){
        $log.debug("go signup");
        SignUpFactory.register({'username':$scope.username, 'password': $scope.password, 'name': $scope.name}).success(function(data){
            $rootScope.storage = $localStorage;
            $rootScope.storage.currentUser = data;
            $state.go("home");
        });



    };
})
    .factory('SignUpFactory', function ($http){
        return {
            register: function(credentials){
                return $http.post('/api/people/signup', credentials);
            }
        }
    });;