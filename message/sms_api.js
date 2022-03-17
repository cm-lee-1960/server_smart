/**
 * nodejs v6.0.0 이상.
 * request v2.34.0 이상.
 * **/

 var crypto = require('crypto');
 var request = require('request');
 
 const defaultEndpoint = 'https://openapis.xroshot.com/V1/';
 
 var salt = function () {
     var salt = '';
     for (var length = 1; length <= 10; length++) {
         salt = salt + Math.floor(Math.random() * 10);
     }
 
     return salt;
 };
 
 var header = function(msgType, apiKey, timestamp) {
     var headers = {
         'API-KEY' : apiKey,
         'SALT' : salt(),
         'TIMESTAMP' : timestamp
     };
 
     if (msgType.indexOf('send') !== -1 && msgType != 'sendSMS') {
         headers['Content-Type'] = 'multipart/form-data';
     } else {
         headers['Content-Type'] = 'application/json; charset=utf-8';
     }
 
     return headers;
 };
 
 var hmac = function (requestBody, salt, hashKey, timestamp) {
     var hmac = crypto.createHmac('sha256', hashKey + '_' + timestamp);
     var message = hmac.update(JSON.stringify(requestBody) + salt).digest('hex');
 
     return message;
 };
 
 var formatedCurrentTimestamp = function () {
     var date = new Date();
     var year = date.getFullYear();
     var month = ('0'+(date.getMonth()+1)).substr(-2);
     var day = ('0'+date.getDate()).substr(-2);
     var hour = ('0'+date.getHours()).substr(-2);
     var minutes = ('0'+date.getMinutes()).substr(-2);
     var seconds = ('0'+date.getSeconds()).substr(-2);
 
     return year + month + day + hour + minutes + seconds;
 };
 
 var message = function (msgType, endpoint, apiKey, hashKey, requestBody, files, callback) {
     var timestamp = formatedCurrentTimestamp();
 
     var headers = header(msgType, apiKey, timestamp);
     headers.HASH = hmac(requestBody, headers.SALT, hashKey, timestamp);
     headers['SECRET-KEY'] = hashKey;
 
     var options = {
         headers : headers
     };
 
     if (endpoint == '') {
         endpoint = defaultEndpoint;
     }
 
     switch (msgType) {
         case 'sendSMS' :
             //options.url = endpoint + 'send/sms';
             options.url = endpoint + 'send/mms';  // 22.03.17) MMS 전송을 위해 임시로 변경
             break;
 
         case 'sendVMS' :
             options.url = endpoint + 'send/vms';
             break;
 
         case 'sendFMS' :
             options.url = endpoint + 'send/fms';
             break;
 
         case 'sendMMS' :
             options.url = endpoint + 'send/mms';
             break;
 
         case 'reserve' :
             options.url = endpoint + 'inquiry/reserve';
             break;
 
         case 'report' :
             options.url = endpoint + 'inquiry/report';
             break;
 
         default :
             options.url = '';
             break;
     }
 
     if (msgType.indexOf('send') !== -1 && msgType != 'sendSMS') {
         var formData = {
             message: {
                 value:  JSON.stringify(requestBody),
                 options: {
                     contentType: 'application/json; charset=utf-8'
                 }
             }
         };
 
         if (files !== undefined && files != '') {
             formData.file = files;
         }
         options.formData = formData;
 
     } else {
         options.json = requestBody;
     }
 
     request.post(options, function(error, response, body) {
         callback(error, response, body);
     });
 };
 
 exports.reserve = function (endpoint, apiKey, hashKey, requestBody, callback) {
     message('reserve', endpoint, apiKey, hashKey, requestBody, '', callback)
 };
 exports.report = function (endpoint, apiKey, hashKey, requestBody, callback) {
     message('report', endpoint, apiKey, hashKey, requestBody, '', callback)
 };
 exports.sendSMS = function (endpoint, apiKey, hashKey, requestBody, callback) {
     message('sendSMS', endpoint, apiKey, hashKey, requestBody, '', callback)
 };
 exports.sendVMS = function (endpoint, apiKey, hashKey, requestBody, files,  callback) {
     message('sendVMS', endpoint, apiKey, hashKey, requestBody, files, callback)
 };
 exports.sendFMS = function (endpoint, apiKey, hashKey, requestBody, files, callback) {
     message('sendFMS', endpoint, apiKey, hashKey, requestBody, files, callback)
 };
 exports.sendMMS = function (endpoint, apiKey, hashKey, requestBody, files, callback) {
     message('sendMMS', endpoint, apiKey, hashKey, requestBody, files, callback)
 };