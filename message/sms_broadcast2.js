/* SMS 동보 */
var sms_api = require('./sms_api');   // 필요한 모듈 호출

///////// 서버 연동에 필요한 키값 할당
const apiKey = '4C08A3B347415C78BEEC7B95BBD5F37E';             			// API Key (from 박하나 과장)
const hashKey = 'new1234!';						// Hash Key (from 박하나 과장)
//const endpoint = 'https://openapi1.xroshot.com/V1/';	// 1센터
//const endpoint = 'https://openapi2.xroshot.com/V1/';	// 2센터
const endpoint = 'https://openapis.xroshot.com/V1/';	// 차세대   /// 차세대만 사용 가능


// POST를 받아 메시지내용, 수신자 정보 획득
// 현재 3000번 포트 Listen
var app = require("express")();
var http = require('http').Server(app);
var bodyParser = require('body-parser');

app.use(bodyParser.json())
app.post('/',function(req,res){
  var message_body = req.body.message;
  var message_receiver = req.body.receiver;

  // res.status(200).send({reponse: 'ok'})
  // http.close();
  
  /////// 메시지 전송을 위한 Body 생성
  var requestBody = {
    MessageType 		: 4,					// 메시지 유형 (1:SMS, 2:VMS, 3:FMS, 4:MMS)
    MessageSubType 		: 1,					// MessageType에 따른 메시지 세부 유형 (1:일반텍스트(SMS,VMS,FMS,MMS), 2:url(SMS,VMS,FMS))
    CallbackNumber 		: '01044700193',		// 회신번호   /// 등록된 번호만 사용 가능 (현재 김종현 차장님 번호)

    //SendNumber 			: '01098880025',		// Option) 발신 과금번호
    ReserveType 		: 1, 					// Option) 예약 타입 (1:즉시 - Default, 2:예약)
    //CustomMessageID 	: 'MSGID_1',			// Option) SP Client에서 지정한 메시지 ID
    //CDRID 			: 'CDRID_1',			// Option) 과금 지정 ID로 다수의 발송 ID(SP_ID)를 가진 경우, CDRID에 입력된 특정 아이디로 과금
    //ReserveTime 		: '20190725163000', 	// Option) 예약 시간 (YYYYMMDDHHMMSS)
    //ReserveDTime 		: '20190725163000',   	// Option) 예약 만료시간 (YYYYMMDDHHMMSS)
    //CDRTime 			: '20190725163000',		// Option) 과금 정산 시간 (YYYYMMDDHHMMSS)
    //CallbackURL 		: '',           	    // Option) 회신 URL

    Message : {
        Content 		: message_body,		// 메시지 내용
        //Subject 		: '메시지 제목',		// Option) 메시지 제목
        Receivers : message_receiver,
    }
  };

  //////// 메시지 전송
  sms_api.sendSMS(endpoint, apiKey, hashKey, requestBody, function(error, response, body) {
    res.status(200).json({reponse: body});
  });

  // 리스닝 종료
  http.close();
  // process.exit();
});

http.listen(3000, function(){
  console.log('listening...');
});