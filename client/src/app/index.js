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
        $urlRouterProvider.otherwise("/");
        $stateProvider.
            state('home', {
                url: '/',
                templateUrl: 'app/templates/home.html',
                controller: 'HomeCtrl'
            })
            .state('match', {
                url: '/match/:matchId',
                templateUrl : 'app/templates/match.html',
                controller: 'MatchCtrl',
                resolve: {
                    match: function (MatchFactory, $stateParams) {
                        return MatchFactory.getMatch($stateParams.matchId);
                    }
                }
            })


    })

.constant('angularMomentConfig', {
    preprocess: 'unix', // optional
    //timezone: 'Australia/Sydney' // optional
})
.run(function(amMoment) {
    amMoment.changeLocale('au');
})

;

