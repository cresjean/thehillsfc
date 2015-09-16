/**
 * Created by crespowang on 25/08/2015.
 */
app.run(function($log,$httpBackend, $http) {

    $httpBackend.whenGET('k/api/matches').respond(function(method, url, data) {
        $log.debug("Faking %s %s", method, url);
        return [200, matches, {}];

    });

    $httpBackend.whenPOST('/api/people/login').respond(function(method, url, data) {
        $log.debug("Faking %s %s", method, url);
        return [200, {username:'su', name:" Nick", admin: true}, {}];

    });


    $httpBackend.whenGET('/api/matches/5197666342404096').respond(function(method, url, data) {
        $log.debug("Faking %s %s", method, url);
        return [200, match, {}];

    });

    $httpBackend.whenGET(/views\/.*/).passThrough();
    $httpBackend.whenGET(/.*/).passThrough(); // catch-all
    $httpBackend.whenPOST(/.*/).passThrough(); // pass through all POSTs
	$httpBackend.whenPUT(/.*/).passThrough();
	$httpBackend.whenDELETE(/.*/).passThrough();
});

var match = {
    "match": {
        "checkinEarliest": 1442710800,
        "checkinLatest": 1442712300,
        "checkinLink": "http://127.0.0.1:8090/checkin/5197666342404096/SYN9KV",
        "createdTime": 1442381996,
        "finishTime": 1442719800,
        "id": "5197666342404096",
        "location": "MacGrade Park",
        "regLink": "http://127.0.0.1:8090/reg/5197666342404096/EQDDKV",
        "startTime": 1442712600
    }
}
;

var matches =
{
    "matches": [
        {
            "checkinEarliest": 1442534400,
            "checkinLatest": 1442535900,
            "createdTime": 1442279584,
            "finishTime": 1442543400,
            "id": "4785074604081152",
            "location": "Cherrybrook",
            "startTime": 1442536200
        },
        {
            "checkinEarliest": 1442723400,
            "checkinLatest": 1442726700,
            "createdTime": 1442278591,
            "finishTime": 1442734200,
            "id": "5066549580791808",
            "location": "Kellyville Plaza",
            "startTime": 1442727000
        },
        {
            "checkinEarliest": 1442721600,
            "checkinLatest": 1442723100,
            "createdTime": 1442279664,
            "finishTime": 1442730600,
            "id": "5910974510923776",
            "location": "Standhope Garden",
            "startTime": 1442723400
        },
        {
            "checkinEarliest": 1443056400,
            "checkinLatest": 1443057900,
            "createdTime": 1442279329,
            "finishTime": 1443065400,
            "id": "6192449487634432",
            "location": "Rouse Hill Sports Centre",
            "startTime": 1443058200
        }
    ]
}


;