console.assert(() => {
    addToLocalStorage("testKey", "testData");
    return localStorage.getItem("testKey") === "testData";
}, "addToLocalStorage test failed");

// Test retrieveFromLocalStorage function
localStorage.setItem("testRetrieveKey", "testRetrieveData");
console.assert(() => {
    return retrieveFromLocalStorage("testRetrieveKey") === "testRetrieveData";
}, "retrieveFromLocalStorage test failed");


console.assert(() => {
    let ajaxCalled = false;
    $.ajax = function(options) {
        ajaxCalled = true;
        options.success();
    };

    logout();

    return ajaxCalled;
}, "logout test failed");

// Test history function
console.assert(() => {
    let ajaxCalled = false;
    $.ajax = function(options) {
        ajaxCalled = true;
        options.success('{"date":"2023-01-01","calories":2000,"burnout":300}');
    };

    history({ target: document.createElement('form') });

    return $("#date").text() === "2023-01-01" && $("#calories").text() === "2000" && $("#burnout").text() === "300" && ajaxCalled;
}, "history test failed");

// Test sendRequest function
console.assert(() => {
    let ajaxCalled = false;
    $.ajax = function(options) {
        ajaxCalled = true;
        options.success('{}');
    };

    sendRequest({}, "testReceiver");

    return ajaxCalled;
}, "sendRequest test failed");

// Test cancelRequest function
console.assert(() => {
    let ajaxCalled = false;
    $.ajax = function(options) {
        ajaxCalled = true;
        options.success('{}');
    };

    cancelRequest({}, "testReceiver");

    return ajaxCalled;
}, "cancelRequest test failed");

// Test approveRequest function 
console.assert(() => {
    let ajaxCalled = false;
    $.ajax = function(options) {
        ajaxCalled = true;
        options.success('{}');
    };

    approveRequest({}, "testReceiver");

    return ajaxCalled;
}, "approveRequest test failed");

// Test dashboard function
console.assert(() => {
    let ajaxCalled = false;
    $.ajax = function(options) {
        ajaxCalled = true;
        options.success('{"enroll":5}');
    };

    dashboard({}, "test@email.com");

    return $("#enroll").text() === "5" && ajaxCalled;
}, "dashboard test failed");
