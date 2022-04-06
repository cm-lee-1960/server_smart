/*
 * 전송결과
 * */
var openapi = require('./sms_api');

const apiKey = '4C08A3B347415C78BEEC7B95BBD5F37E';             			// API Key
const hashKey = 'new1234!';						// Hash Key
//const endpoint = 'https://openapi1.xroshot.com/V1/';	// 1센터
//const endpoint = 'https://openapi2.xroshot.com/V1/';	// 2센터
const endpoint = 'https://openapis.xroshot.com/V1/';	// 차세대

// POST를 받아 메시지내용, 수신자 정보 획득
// 현재 3000번 포트 Listen
var app = require("express")();
var http = require('http').Server(app);
var bodyParser = require('body-parser');

app.use(bodyParser.json())
app.post('/',function(req,res){
  var JobID_list = req.body.JobIDs;
  var send_day = req.body.SendDay;
  var requestBody = {
    JobIDs      : JobID_list,     // JobID 배열
    SendDay     : send_day       // 차세대 일때만 필수) JobID 리스트 발송 날짜
  };
  openapi.report(endpoint, apiKey, hashKey, requestBody, function(error, response, body) {
    res.status(200).json({response: body});
  });

  http.close();
  });
  
  http.listen(3000, function(){
  console.log('listening...');
  });
