'use strict';

var app = angular.module('hillfc',
    [
        'ui.router',
        'ui.bootstrap',
        'ngMockE2E',
        'ngAnimate',
        'angularUtils.directives.dirPagination',
        'ui.bootstrap.datetimepicker',
        'angularMoment'
    ]);

app.config(function($stateProvider, $urlRouterProvider){
        $urlRouterProvider.otherwise("/login");
        $stateProvider
            .state('login', {
                url: '^/login',
                templateUrl: 'app/templates/login.html',
                controller: 'LoginCtrl'
            })
            .state('home', {
                url: '^/home',
                templateUrl: 'app/templates/home.html',
                controller: 'HomeCtrl',
                resolve: {
                        LoginFact: 'LoginFactory',
						loginSession: function($q, $log, LoginFact) {
                            var deferred = $q.defer();
                            $log.debug("getting login session");
                            var loginStatus =  LoginFact.getLoginStatus();
                            $log.debug("login s " + loginStatus);
                            if (loginStatus == false){
                                $log.debug("login looks bad");
                                deferred.reject('Please login first');
                            }
                            else
                            {
                                $log.debug("login looks good");
                                deferred.resolve();
                            }
                            return deferred.promise;
						}
                }
            })
            .state('match', {
                url: '/match/:matchId',
                templateUrl : 'app/templates/match.html',
                controller: 'MatchCtrl',
                resolve: {
                    match: function (MatchFactory, $stateParams) {
                        return MatchFactory.getMatch($stateParams.matchId);
                    },
                    LoginFact: 'LoginFactory',
						loginSession: function($q, $log, LoginFact) {
                            var deferred = $q.defer();
                            $log.debug("getting login session");
                            var loginStatus =  LoginFact.getLoginStatus();
                            $log.debug("login s " + loginStatus);
                            if (loginStatus == false){
                                $log.debug("login looks bad");
                                deferred.reject('Please login first');
                            }
                            else
                            {
                                $log.debug("login looks good");
                                deferred.resolve();
                            }
                            return deferred.promise;
						}
                }
            })


    })

.constant('angularMomentConfig', {
    preprocess: 'unix', // optional
    //timezone: 'Australia/Sydney' // optional
})
.run(function(amMoment, $rootScope, $state, $log) {
        $rootScope.$on('$stateChangeError', function(event, toState, toParams, fromState, fromParams, error){
            $log.debug("state change error");
		$state.go('login');

	});
    amMoment.changeLocale('au');
})

;

