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


    })

.constant('angularMomentConfig', {
    preprocess: 'unix', // optional
    //timezone: 'Australia/Sydney' // optional
})
.run(function(amMoment) {
    amMoment.changeLocale('au');
})

.directive('input-datetime', function() {
  return {
    require: 'ngModel',
    link: function(scope, element, attrs, ngModelController) {
      ngModelController.$parsers.push(function(data) {
        //convert data from view format to model format
        return data; //converted
      });

      ngModelController.$formatters.push(function(data) {
        //convert data from model format to view format
          var reformat = moment(data).format('yyyy');
          return reformat; //converted
      });
    }
  }
});
;

