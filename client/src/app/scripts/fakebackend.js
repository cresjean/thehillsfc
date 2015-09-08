/**
 * Created by crespowang on 25/08/2015.
 */
app.run(function($log,$httpBackend, $http) {

    $httpBackend.whenGET('d/api/matches').respond(function(method, url, data) {
        $log.debug("Faking %s %s", method, url);
        return [200, matches, {}];

    });


    $httpBackend.whenGET('d/api/matches/5066549580791808').respond(function(method, url, data) {
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
        "checkinEarliest": 1440923400,
        "checkinLatest": 1440926700,
        "createdTime": 1440568432,
        "finishTime": 1440934200,
        "id": "5891733057437696",
        "location": "Burwood",
        "startTime": 1440927000
    }
};

var matches =
{
    "matches": [
        {
            "checkinEarliest": 1439350200,
            "checkinLatest": 1439353500,
            "created": 1440566592,
            "finishTime": 1439361000,
            "id": "5066549580791808",
            "location": "Kellyville Plaza",
            "startTime": 1440566611
        },
        {
            "checkinEarliest": 1439350200,
            "checkinLatest": 1439353500,
            "created": 1440561042,
            "finishTime": 1439361000,
            "id": "5275456790069248",
            "location": "Kellyville Plaza",
            "startTime": 1439353800
        },
        {
            "checkinEarliest": 1439350200,
            "checkinLatest": 1439353500,
            "created": 1440560229,
            "finishTime": 1439361000,
            "id": "5629499534213120",
            "location": "Kellyville Plaza",
            "startTime": 1439353800
        },
        {
            "checkinEarliest": 1439350200,
            "checkinLatest": 1439353500,
            "created": 1440560898,
            "finishTime": 1439361000,
            "id": "5838406743490560",
            "location": "Kellyville Plaza",
            "startTime": 1439353800
        },
        {
            "checkinEarliest": 1439350200,
            "checkinLatest": 1439353500,
            "created": 1440561137,
            "finishTime": 1439361000,
            "id": "6401356696911872",
            "location": "Kellyville Plaza",
            "startTime": 1439353800
        }
    ]
}

;