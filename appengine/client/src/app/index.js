'use strict';

var app = angular.module('hillfc',
    [
        'ui.router',
        'ui.bootstrap',
        'ngMockE2E',
        'ngAnimate',
        'ngStorage',
        'angularUtils.directives.dirPagination',
        'ui.bootstrap.datetimepicker',
        'angularMoment',
        'monospaced.qrcode',
        'frapontillo.bootstrap-switch',
        'ui.select',
      'gridshore.c3js.chart',
      'angular-dazhaohu'
    ]);

app.config(function($stateProvider, $urlRouterProvider, $httpProvider){
    $urlRouterProvider.otherwise("/home");

    $stateProvider
        .state('match-signup', {
            url: '^/match-signup/:matchId/:matchCode',
            controller: 'SignUpMatchCtrl',
            templateUrl: 'app/templates/match-signup.html',
            resolve:{
                match: function (MatchFactory, $stateParams) {
                    return MatchFactory.signUp($stateParams.matchId, $stateParams.matchCode);
                }
            },
            data: {
                requireLogin: true
            }
        })
        .state('match-signin', {
            url: '^/match-signin/:matchId',
            abstract: true,
            controller: 'SignInMatchCtrl',
            templateUrl: 'app/templates/match-signin.html',
            resolve:{
                match: function (MatchFactory, $stateParams) {
                    return MatchFactory.getMatch($stateParams.matchId);
                }
            },
            data: {
                requireLogin: true
            }
        })
        .state('match-signin.success', {
            url: '/success',
            controller: 'SignInMatchCtrl',
            templateUrl: 'app/templates/match-signin-success.html'
        })
        .state('match-signin.early', {
            url: '/early',
            controller: 'SignInMatchCtrl',
            templateUrl: 'app/templates/match-signin-early.html'
        })
        .state('match-signin.late', {
            url: '/late',
            controller: 'SignInMatchCtrl',
            templateUrl: 'app/templates/match-signin-late.html'
        })
        .state('match-signin.dup', {
            url: '/dup',
            controller: 'SignInMatchCtrl',
            templateUrl: 'app/templates/match-signin-dup.html'
        })
        .state('new', {
            url : '^/new-match',
            controller: 'NewMatchCtrl',
            templateUrl: 'app/templates/new-match.html',
            data: {
                requireAdmin: true,
                requireLogin: true
            }
        })
        .state('logout', {
            url: '^/logout',
            controller: 'LogoutCtrl',
            data: {
                requireLogin: false
            }
        })
        .state('settings', {
            url: '^/settings',
            controller: 'SettingsCtrl',
            templateUrl: 'app/templates/settings.html',
            data: {
                requireLogin: false
            },
            resolve:{
                me: function (SettingsFactory) {
                    return SettingsFactory.getMe();
                }
            }
        })
        .state('login', {
            url: '^/login?next',
            templateUrl: 'app/templates/login.html',
            controller: 'LoginCtrl',
            data: {
                requireLogin: false
            }
        })
        .state('password-reset', {
            url: '^/password-reset',
            templateUrl: 'app/templates/password-reset.html',
            controller: 'PasswordResetCtrl',
            data: {
                requireLogin: false
            }
        })
        .state('signup', {
            url: '^/signup',
            templateUrl: 'app/templates/signup.html',
            controller: 'SignUpCtrl',
            data: {
                requireLogin: false
            }
        })
        .state('billboard', {
          url: '^/billboard',
          templateUrl: 'app/templates/billboard.html',
          controller: 'BillboardCtrl',
          data: {
            requireLogin: true
          }
        })
        .state('home', {
            url: '^/home',
            templateUrl: 'app/templates/home.html',
            controller: 'HomeCtrl',
            data: {
                requireLogin: true
            },
            resolve: {
              MeStat : function(MeFactory) {
                    return MeFactory.getStat();

              }
            }
            //resolve: {
            //        LoginFact: 'LoginFactory',
            //	loginSession: function($q, $log, LoginFact) {
            //            var deferred = $q.defer();
            //            $log.debug("getting login session");
            //            var loginStatus =  LoginFact.getLoginStatus();
            //            $log.debug("login s " + loginStatus);
            //            if (loginStatus == false){
            //                $log.debug("login looks bad");
            //                deferred.reject('Please login first');
            //            }
            //            else
            //            {
            //                $log.debug("login looks good");
            //                deferred.resolve();
            //            }
            //            return deferred.promise;
            //	}
            //}
        })
        .state('match', {
            url: '/match/:matchId',
            templateUrl : 'app/templates/match.html',
            controller: 'MatchCtrl',
            data: {
                requireLogin: true
            },
            resolve: {
                match: function (MatchFactory, $stateParams) {
                    return MatchFactory.getMatch($stateParams.matchId);
                },
                isIn: function (MatchFactory, $stateParams, $rootScope) {
                    return MatchFactory.getPlayer($stateParams.matchId, $rootScope.storage.currentUser.id)
                },
                players: function(MatchFactory, $stateParams){
                    return MatchFactory.getPlayers($stateParams.matchId)

                }
            }

        });
  //
  //$httpProvider.interceptors.push(function($q, $injector) {
  //        return {
  //
  //            'responseError': function(rejection){
  //
  //                var defer = $q.defer();
  //
  //                if(rejection.status == 401){
  //                  $injector.get('$state').transitionTo('login');
  //                }
  //
  //                defer.reject(rejection);
  //
  //                return defer.promise;
  //
  //            }
  //        };
  //    });
  //

})

    .constant('angularMomentConfig', {
        preprocess: 'unix', // optional
        timezone: 'Australia/Sydney' // optional
    })
    .run(function(amMoment, $rootScope, $state, $log, $localStorage) {
        $rootScope.storage = $localStorage;


        $rootScope.$on('$stateChangeStart', function (event, toState, toParams) {
            var requireLogin = toState.data.requireLogin;
            var requireAdmin = toState.data.requireAdmin;
            $log.debug("State Change Start");
            if (requireLogin && typeof $rootScope.storage.currentUser === 'undefined') {
                event.preventDefault();
                $state.go('login');
            }
            else if(requireAdmin && $rootScope.storage.currentUser.admin === false){

                event.preventDefault();
                $state.go('home');
            }

        });
        $rootScope.$on('$stateChangeError', function(event, toState, toParams, fromState, fromParams, error){
            $log.debug("State Change Error");

        if(error.status == 401){
          $log.debug("401 detected. Redirecting...");
            $rootScope.storage.currentUser = undefined;
            $state.go("login");
        }
    });

        amMoment.changeLocale('au');
    })
;
