/*
 * SMS 동보
 * */
var sms_api = require('./sms_api');   // 필요한 모듈 호출

///////// 서버 연동에 필요한 키값 할당
const apiKey = '4C08A3B347415C78BEEC7B95BBD5F37E';             			// API Key (from 박하나 과장)
const hashKey = 'new1234!';						// Hash Key (from 박하나 과장)
//const endpoint = 'https://openapi1.xroshot.com/V1/';	// 1센터
//const endpoint = 'https://openapi2.xroshot.com/V1/';	// 2센터
const endpoint = 'https://openapis.xroshot.com/V1/';	// 차세대   /// 차세대만 사용 가능

///////// DB 연동
var mysql      = require('mysql');  
var connection = mysql.createConnection({  
  host     : '127.0.0.1',
  port     : '3306',
  user     : 'smartnqi',  
  password : 'nwai1234!',  
  database : 'smart'  
});  


//////// DB에서 데이터 가져오기
//////// requestBody의 Message와 Receivers 부분에 데이터 전달
connection.connect(function(err){
    if(!err) {  
        console.log("Database is connected ... \n\n");
    } else {
        console.log("Error connecting database ... \n\n");
    }
});
connection.query('SELECT * from smart.message_sentxroshotmessage ORDER BY ID DESC LIMIT 1', function(err, rows, fields) {
    if (!err){
        let message_body = rows[0].message;   /// Message 내용
        var message_number = rows[0].receiver.replace(/\s+/g, '').split(',');
        var list_length = message_number.length;
        var message_receiver = [];
        for (var i=1 ; i<=list_length; i++){
            var receivers_dict = {'Seq' : i, 'Number' : message_number[i-1]};
            message_receiver.push(receivers_dict);   /// 수신자 리스트
		}

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
            console.log(body);
        }); 
	}
});

connection.query('delete from smart.message_sentxroshotmessage', function(err, result) {
    if (err) throw err;
    console.log('sended message will be deleted')
});
connection.end();




