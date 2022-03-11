
// 리포트데이터 정제		
var total1 = parseInt(document.getElementById("5tt").outerText);
var total2 = parseInt(document.getElementById("ltt").outerText);
var total3 = parseInt(document.getElementById("witt").outerText);
var total4 = parseInt(document.getElementById("wtt").outerText);
var total5 = parseInt(document.getElementById("5nj").outerText);
var total6 = parseInt(document.getElementById("lnj").outerText);
var total7 = parseInt(document.getElementById("winj").outerText);
var total8 = parseInt(document.getElementById("wnj").outerText);

document.getElementById("tt1").innerHTML = total1+"개 지역 중";
document.getElementById("tt2").innerHTML = total2+"개 지역 중";
document.getElementById("tt3").innerHTML = total3+"개 지역 중";
document.getElementById("tt4").innerHTML = total4+"개 지역 중";
document.getElementById("pc1").innerHTML = "(" + ((total5/total1)*100).toFixed(2) + "%)";
document.getElementById("pc2").innerHTML = "(" + ((total6/total2)*100).toFixed(2) + "%)";
document.getElementById("pc3").innerHTML = "(" + ((total7/total3)*100).toFixed(2) + "%)";
document.getElementById("pc4").innerHTML = "(" + ((total8/total4)*100).toFixed(2) + "%)";
document.getElementById("tt").innerHTML = total1+total2+total3+total4+"개";
document.getElementById("ttf").innerHTML = total5+total6+total7+total8+"개";
document.getElementById("pcf").innerHTML = "(진도율:" + (((total5+total6+total7+total8)/(total1+total2+total3+total4))*100).toFixed(2) + "%)";


var hjd5gseoul = parseInt(document.getElementById("hjd5gseoul").outerText);
var hjd5gincheon = parseInt(document.getElementById("hjd5gincheon").outerText);
var hjd5gulsan = parseInt(document.getElementById("hjd5gulsan").outerText);
var hjd5gdaegu = parseInt(document.getElementById("hjd5gdaegu").outerText);
var hjd5ggwangju = parseInt(document.getElementById("hjd5ggwangju").outerText);
var hjd5gdaejun = parseInt(document.getElementById("hjd5gdaejun").outerText);
var hjd5ggyunggi = parseInt(document.getElementById("hjd5ggyunggi").outerText);
var hjd5ggyungbuk = parseInt(document.getElementById("hjd5ggyungbuk").outerText);
var hjd5gjunnam = parseInt(document.getElementById("hjd5gjunnam").outerText);
var hjd5gjunbuk = parseInt(document.getElementById("hjd5gjunbuk").outerText);
var hjd5gchungnam = parseInt(document.getElementById("hjd5gchungnam").outerText);
var hjd5gchungbuk = parseInt(document.getElementById("hjd5gchungbuk").outerText);
var hjd5gsejong = parseInt(document.getElementById("hjd5gsejong").outerText);
var dagyo5gseoul = parseInt(document.getElementById("dagyo5gseoul").outerText);
var dagyo5gincheon = parseInt(document.getElementById("dagyo5gincheon").outerText);
var dagyo5gulsan = parseInt(document.getElementById("dagyo5gulsan").outerText);
var dagyo5gdaegu = parseInt(document.getElementById("dagyo5gdaegu").outerText);
var dagyo5ggwangju = parseInt(document.getElementById("dagyo5ggwangju").outerText);
var dagyo5gdaejun = parseInt(document.getElementById("dagyo5gdaejun").outerText);
var dagyo5ggyunggi = parseInt(document.getElementById("dagyo5ggyunggi").outerText);
var dagyo5ggyungbuk = parseInt(document.getElementById("dagyo5ggyungbuk").outerText);
var dagyo5gjunnam = parseInt(document.getElementById("dagyo5gjunnam").outerText);
var dagyo5gjunbuk = parseInt(document.getElementById("dagyo5gjunbuk").outerText);
var dagyo5gchungnam = parseInt(document.getElementById("dagyo5gchungnam").outerText);
var dagyo5gchungbuk = parseInt(document.getElementById("dagyo5gchungbuk").outerText);
var dagyo5gsejong = parseInt(document.getElementById("dagyo5gsejong").outerText);
var dagyo5gsudo = parseInt(document.getElementById("dagyo5gsudo").outerText);

var bigcityLTEseoul=parseInt(document.getElementById('bigcityLTEseoul').outerText);
var bigcityLTEincheon=parseInt(document.getElementById('bigcityLTEincheon').outerText);
var bigcityLTEulsan=parseInt(document.getElementById('bigcityLTEulsan').outerText);
var bigcityLTEdaegu=parseInt(document.getElementById('bigcityLTEdaegu').outerText);
var bigcityLTEgwangju=parseInt(document.getElementById('bigcityLTEgwangju').outerText);
var bigcityLTEdaejun=parseInt(document.getElementById('bigcityLTEdaejun').outerText);
var bigcityLTEgyunggi=parseInt(document.getElementById('bigcityLTEgyunggi').outerText);
var bigcityLTEgyungbuk=parseInt(document.getElementById('bigcityLTEgyungbuk').outerText);
var bigcityLTEjunnam=parseInt(document.getElementById('bigcityLTEjunnam').outerText);
var bigcityLTEjunbuk=parseInt(document.getElementById('bigcityLTEjunbuk').outerText);
var bigcityLTEchungnam=parseInt(document.getElementById('bigcityLTEchungnam').outerText);
var bigcityLTEchungbuk=parseInt(document.getElementById('bigcityLTEchungbuk').outerText);
var bigcityLTEsejong=parseInt(document.getElementById('bigcityLTEsejong').outerText);
var bigcityLTEsudo=parseInt(document.getElementById('bigcityLTEsudo').outerText);
var smallcityLTEseoul=parseInt(document.getElementById('smallcityLTEseoul').outerText);
var smallcityLTEincheon=parseInt(document.getElementById('smallcityLTEincheon').outerText);
var smallcityLTEulsan=parseInt(document.getElementById('smallcityLTEulsan').outerText);
var smallcityLTEdaegu=parseInt(document.getElementById('smallcityLTEdaegu').outerText);
var smallcityLTEgwangju=parseInt(document.getElementById('smallcityLTEgwangju').outerText);
var smallcityLTEdaejun=parseInt(document.getElementById('smallcityLTEdaejun').outerText);
var smallcityLTEgyunggi=parseInt(document.getElementById('smallcityLTEgyunggi').outerText);
var smallcityLTEgyungbuk=parseInt(document.getElementById('smallcityLTEgyungbuk').outerText);
var smallcityLTEjunnam=parseInt(document.getElementById('smallcityLTEjunnam').outerText);
var smallcityLTEjunbuk=parseInt(document.getElementById('smallcityLTEjunbuk').outerText);
var smallcityLTEchungnam=parseInt(document.getElementById('smallcityLTEchungnam').outerText);
var smallcityLTEchungbuk=parseInt(document.getElementById('smallcityLTEchungbuk').outerText);
var smallcityLTEsejong=parseInt(document.getElementById('smallcityLTEsejong').outerText);
var smallcityLTEsudo=parseInt(document.getElementById('smallcityLTEsudo').outerText);
var nongLTEseoul=parseInt(document.getElementById('nongLTEseoul').outerText);
var nongLTEincheon=parseInt(document.getElementById('nongLTEincheon').outerText);
var nongLTEulsan=parseInt(document.getElementById('nongLTEulsan').outerText);
var nongLTEdaegu=parseInt(document.getElementById('nongLTEdaegu').outerText);
var nongLTEgwangju=parseInt(document.getElementById('nongLTEgwangju').outerText);
var nongLTEdaejun=parseInt(document.getElementById('nongLTEdaejun').outerText);
var nongLTEgyunggi=parseInt(document.getElementById('nongLTEgyunggi').outerText);
var nongLTEgyungbuk=parseInt(document.getElementById('nongLTEgyungbuk').outerText);
var nongLTEjunnam=parseInt(document.getElementById('nongLTEjunnam').outerText);
var nongLTEjunbuk=parseInt(document.getElementById('nongLTEjunbuk').outerText);
var nongLTEchungnam=parseInt(document.getElementById('nongLTEchungnam').outerText);
var nongLTEchungbuk=parseInt(document.getElementById('nongLTEchungbuk').outerText);
var nongLTEsejong=parseInt(document.getElementById('nongLTEsejong').outerText);
var nongLTEsudo=parseInt(document.getElementById('nongLTEsudo').outerText);
var inbuildingLTEcdys=parseInt(document.getElementById('inbuildingLTEcdys').outerText);
var inbuildingLTEdhbw=parseInt(document.getElementById('inbuildingLTEdhbw').outerText);
var inbuildingLTEbhj=parseInt(document.getElementById('inbuildingLTEbhj').outerText);
var inbuildingLTEtmn=parseInt(document.getElementById('inbuildingLTEtmn').outerText);
var inbuildingLTEgh=parseInt(document.getElementById('inbuildingLTEgh').outerText);
var inbuildingLTEdhjp=parseInt(document.getElementById('inbuildingLTEdhjp').outerText);
var inbuildingLTEjsj=parseInt(document.getElementById('inbuildingLTEjsj').outerText);
var inbuildingLTEjhcys=parseInt(document.getElementById('inbuildingLTEjhcys').outerText);
var themeLTEjunnam=parseInt(document.getElementById('themeLTEjunnam').outerText);
var themeLTEjunbuk=parseInt(document.getElementById('themeLTEjunbuk').outerText);
var themeLTEchungnam=parseInt(document.getElementById('themeLTEchungnam').outerText);
var themeLTEchungbuk=parseInt(document.getElementById('themeLTEchungbuk').outerText);
var themeLTEsejong=parseInt(document.getElementById('themeLTEsejong').outerText);
// var sangWiFiseoul=parseInt(document.getElementById('sangWiFiseoul').outerText);
// var sangWiFiincheon=parseInt(document.getElementById('sangWiFiincheon').outerText);
// var sangWiFiulsan=parseInt(document.getElementById('sangWiFiulsan').outerText);
// var sangWiFidaegu=parseInt(document.getElementById('sangWiFidaegu').outerText);
// var sangWiFigwangju=parseInt(document.getElementById('sangWiFigwangju').outerText);
// var sangWiFidaejun=parseInt(document.getElementById('sangWiFidaejun').outerText);
// var sangWiFigyunggi=parseInt(document.getElementById('sangWiFigyunggi').outerText);
// var sangWiFigyungbuk=parseInt(document.getElementById('sangWiFigyungbuk').outerText);
// var sangWiFijunnam=parseInt(document.getElementById('sangWiFijunnam').outerText);
// var sangWiFijunbuk=parseInt(document.getElementById('sangWiFijunbuk').outerText);
// var sangWiFichungnam=parseInt(document.getElementById('sangWiFichungnam').outerText);
// var sangWiFichungbuk=parseInt(document.getElementById('sangWiFichungbuk').outerText);
// var sangWiFisejong=parseInt(document.getElementById('sangWiFisejong').outerText);
// var sangWiFisudo=parseInt(document.getElementById('sangWiFisudo').outerText);
// var gaeWiFiseoul=parseInt(document.getElementById('gaeWiFiseoul').outerText);
// var gaeWiFiincheon=parseInt(document.getElementById('gaeWiFiincheon').outerText);
// var gaeWiFiulsan=parseInt(document.getElementById('gaeWiFiulsan').outerText);
// var gaeWiFidaegu=parseInt(document.getElementById('gaeWiFidaegu').outerText);
// var gaeWiFigwangju=parseInt(document.getElementById('gaeWiFigwangju').outerText);
// var gaeWiFidaejun=parseInt(document.getElementById('gaeWiFidaejun').outerText);
// var gaeWiFigyunggi=parseInt(document.getElementById('gaeWiFigyunggi').outerText);
// var gaeWiFigyungbuk=parseInt(document.getElementById('gaeWiFigyungbuk').outerText);
// var gaeWiFijunnam=parseInt(document.getElementById('gaeWiFijunnam').outerText);
// var gaeWiFijunbuk=parseInt(document.getElementById('gaeWiFijunbuk').outerText);
// var gaeWiFichungnam=parseInt(document.getElementById('gaeWiFichungnam').outerText);
// var gaeWiFichungbuk=parseInt(document.getElementById('gaeWiFichungbuk').outerText);
// var gaeWiFisejong=parseInt(document.getElementById('gaeWiFisejong').outerText);
// var gaeWiFisudo=parseInt(document.getElementById('gaeWiFisudo').outerText);
// var weakseoul=parseInt(document.getElementById('weakseoul').outerText);
// var weakincheon=parseInt(document.getElementById('weakincheon').outerText);
// var weakulsan=parseInt(document.getElementById('weakulsan').outerText);
// var weakdaegu=parseInt(document.getElementById('weakdaegu').outerText);
// var weakgwangju=parseInt(document.getElementById('weakgwangju').outerText);
// var weakdaejun=parseInt(document.getElementById('weakdaejun').outerText);
// var weakgyunggi=parseInt(document.getElementById('weakgyunggi').outerText);
// var weakgyungbuk=parseInt(document.getElementById('weakgyungbuk').outerText);
// var weakjunnam=parseInt(document.getElementById('weakjunnam').outerText);
// var weakjunbuk=parseInt(document.getElementById('weakjunbuk').outerText);
// var weakchungnam=parseInt(document.getElementById('weakchungnam').outerText);
// var weakchungbuk=parseInt(document.getElementById('weakchungbuk').outerText);
// var weaksejong=parseInt(document.getElementById('weaksejong').outerText);
// var weaksudo=parseInt(document.getElementById('weaksudo').outerText);

if (hjd5gseoul > 0) {
    document.getElementById("hjd5gseoul").innerHTML = " 서울 " + hjd5gseoul;
    
} else {
    document.getElementById("hjd5gseoul").innerHTML = "";
}
if (hjd5gincheon > 0) {
    document.getElementById("hjd5gincheon").innerHTML = " 인천 " + hjd5gincheon;
    
} else {
    document.getElementById("hjd5gincheon").innerHTML = "";
}
if (hjd5gulsan > 0) {
    document.getElementById("hjd5gulsan").innerHTML = " 울산 " + hjd5gulsan;
    
} else {
    document.getElementById("hjd5gulsan").innerHTML = "";
}
if (hjd5gdaegu > 0) {
    document.getElementById("hjd5gdaegu").innerHTML = " 대구 " + hjd5gdaegu;
    
} else {
    document.getElementById("hjd5gdaegu").innerHTML = "";
}
if (hjd5ggwangju > 0) {
    document.getElementById("hjd5ggwangju").innerHTML = " 광주 " + hjd5ggwangju;
    
} else {
    document.getElementById("hjd5ggwangju").innerHTML = "";
}
if (hjd5gdaejun > 0) {
    document.getElementById("hjd5gdaejun").innerHTML = " 대전 " + hjd5gdaejun;
    
} else {
    document.getElementById("hjd5gdaejun").innerHTML = "";
}
if (hjd5ggyunggi > 0) {
    document.getElementById("hjd5ggyunggi").innerHTML = " 경기 " + hjd5ggyunggi;
    
} else {
    document.getElementById("hjd5ggyunggi").innerHTML = "";
}
if (hjd5ggyungbuk > 0) {
    document.getElementById("hjd5ggyungbuk").innerHTML = " 경북 " + hjd5ggyungbuk;
    
} else {
    document.getElementById("hjd5ggyungbuk").innerHTML = "";
}
if (hjd5gjunnam > 0) {
    document.getElementById("hjd5gjunnam").innerHTML = " 전남 " + hjd5gjunnam;
    
} else {
    document.getElementById("hjd5gjunnam").innerHTML = "";
}
if (hjd5gjunbuk > 0) {
    document.getElementById("hjd5gjunbuk").innerHTML = " 전북 " + hjd5gjunbuk;
    
} else {
    document.getElementById("hjd5gjunbuk").innerHTML = "";
}
if (hjd5gchungnam > 0) {
    document.getElementById("hjd5gchungnam").innerHTML = " 충남 " + hjd5gchungnam;
    
} else {
    document.getElementById("hjd5gchungnam").innerHTML = "";
}
if (hjd5gchungbuk > 0) {
    document.getElementById("hjd5gchungbuk").innerHTML = " 충북 " + hjd5gchungbuk;
    
} else {
    document.getElementById("hjd5gchungbuk").innerHTML = "";
}
if (hjd5gsejong > 0) {
    document.getElementById("hjd5gsejong").innerHTML = " 세종 " + hjd5gsejong;
    
} else {
    document.getElementById("hjd5gsejong").innerHTML = "";
}
if (dagyo5gseoul > 0) {
    document.getElementById("dagyo5gseoul").innerHTML = " 서울 " + dagyo5gseoul;
    
} else {
    document.getElementById("dagyo5gseoul").innerHTML = "";
}
if (dagyo5gincheon > 0) {
    document.getElementById("dagyo5gincheon").innerHTML = " 인천 " + dagyo5gincheon;
    
} else {
    document.getElementById("dagyo5gincheon").innerHTML = "";
}
if (dagyo5gulsan > 0) {
    document.getElementById("dagyo5gulsan").innerHTML = " 울산 " + dagyo5gulsan;
    
} else {
    document.getElementById("dagyo5gulsan").innerHTML = "";
}
if (dagyo5gdaegu > 0) {
    document.getElementById("dagyo5gdaegu").innerHTML = " 대구 " + dagyo5gdaegu;
    
} else {
    document.getElementById("dagyo5gdaegu").innerHTML = "";
}
if (dagyo5ggwangju > 0) {
    document.getElementById("dagyo5ggwangju").innerHTML = " 광주 " + dagyo5ggwangju;
    
} else {
    document.getElementById("dagyo5ggwangju").innerHTML = "";
}
if (dagyo5gdaejun > 0) {
    document.getElementById("dagyo5gdaejun").innerHTML = " 대전 " + dagyo5gdaejun;
    
} else {
    document.getElementById("dagyo5gdaejun").innerHTML = "";
}
if (dagyo5ggyunggi > 0) {
    document.getElementById("dagyo5ggyunggi").innerHTML = " 경기 " + dagyo5ggyunggi;
    
} else {
    document.getElementById("dagyo5ggyunggi").innerHTML = "";
}
if (dagyo5ggyungbuk > 0) {
    document.getElementById("dagyo5ggyungbuk").innerHTML = " 경북 " + dagyo5ggyungbuk;
    
} else {
    document.getElementById("dagyo5ggyungbuk").innerHTML = "";
}
if (dagyo5gjunnam > 0) {
    document.getElementById("dagyo5gjunnam").innerHTML = " 전남 " + dagyo5gjunnam;
    
} else {
    document.getElementById("dagyo5gjunnam").innerHTML = "";
}
if (dagyo5gjunbuk > 0) {
    document.getElementById("dagyo5gjunbuk").innerHTML = " 전북 " + dagyo5gjunbuk;
    
} else {
    document.getElementById("dagyo5gjunbuk").innerHTML = "";
}
if (dagyo5gchungnam > 0) {
    document.getElementById("dagyo5gchungnam").innerHTML = " 충남 " + dagyo5gchungnam;
    
} else {
    document.getElementById("dagyo5gchungnam").innerHTML = "";
}
if (dagyo5gchungbuk > 0) {
    document.getElementById("dagyo5gchungbuk").innerHTML = " 충북 " + dagyo5gchungbuk;
    
} else {
    document.getElementById("dagyo5gchungbuk").innerHTML = "";
}
if (dagyo5gsejong > 0) {
    document.getElementById("dagyo5gsejong").innerHTML = " 세종 " + dagyo5gsejong;
    
} else {
    document.getElementById("dagyo5gsejong").innerHTML = "";
}
if (dagyo5gsudo > 0) {
    document.getElementById("dagyo5gsudo").innerHTML = " 수도권 " + dagyo5gsudo;
    
} else {
    document.getElementById("dagyo5gsudo").innerHTML = "";
}


if (bigcityLTEseoul > 0) {
    document.getElementById("bigcityLTEseoul").innerHTML = " 서울 " + bigcityLTEseoul;
    
} else {
    document.getElementById("bigcityLTEseoul").innerHTML = "";
}
if (bigcityLTEincheon > 0) {
    document.getElementById("bigcityLTEincheon").innerHTML = " 인천 " + bigcityLTEincheon;
    
} else {
    document.getElementById("bigcityLTEincheon").innerHTML = "";
}
if (bigcityLTEulsan > 0) {
    document.getElementById("bigcityLTEulsan").innerHTML = " 울산 " + bigcityLTEulsan;
    
} else {
    document.getElementById("bigcityLTEulsan").innerHTML = "";
}
if (bigcityLTEdaegu > 0) {
    document.getElementById("bigcityLTEdaegu").innerHTML = " 대구 " + bigcityLTEdaegu;
    
} else {
    document.getElementById("bigcityLTEdaegu").innerHTML = "";
}
if (bigcityLTEgwangju > 0) {
    document.getElementById("bigcityLTEgwangju").innerHTML = " 광주 " + bigcityLTEgwangju;
    
} else {
    document.getElementById("bigcityLTEgwangju").innerHTML = "";
}
if (bigcityLTEdaejun > 0) {
    document.getElementById("bigcityLTEdaejun").innerHTML = " 대전 " + bigcityLTEdaejun;
    
} else {
    document.getElementById("bigcityLTEdaejun").innerHTML = "";
}
if (bigcityLTEgyunggi > 0) {
    document.getElementById("bigcityLTEgyunggi").innerHTML = " 경기 " + bigcityLTEgyunggi;
    
} else {
    document.getElementById("bigcityLTEgyunggi").innerHTML = "";
}
if (bigcityLTEgyungbuk > 0) {
    document.getElementById("bigcityLTEgyungbuk").innerHTML = " 경북 " + bigcityLTEgyungbuk;
    
} else {
    document.getElementById("bigcityLTEgyungbuk").innerHTML = "";
}
if (bigcityLTEjunnam > 0) {
    document.getElementById("bigcityLTEjunnam").innerHTML = " 전남 " + bigcityLTEjunnam;
    
} else {
    document.getElementById("bigcityLTEjunnam").innerHTML = "";
}
if (bigcityLTEjunbuk > 0) {
    document.getElementById("bigcityLTEjunbuk").innerHTML = " 전북 " + bigcityLTEjunbuk;
    
} else {
    document.getElementById("bigcityLTEjunbuk").innerHTML = "";
}
if (bigcityLTEchungnam > 0) {
    document.getElementById("bigcityLTEchungnam").innerHTML = " 충남 " + bigcityLTEchungnam;
    
} else {
    document.getElementById("bigcityLTEchungnam").innerHTML = "";
}
if (bigcityLTEchungbuk > 0) {
    document.getElementById("bigcityLTEchungbuk").innerHTML = " 충북 " + bigcityLTEchungbuk;
    
} else {
    document.getElementById("bigcityLTEchungbuk").innerHTML = "";
}
if (bigcityLTEsejong > 0) {
    document.getElementById("bigcityLTEsejong").innerHTML = " 세종 " + bigcityLTEsejong;
    
} else {
    document.getElementById("bigcityLTEsejong").innerHTML = "";
}
if (bigcityLTEsudo > 0) {
    document.getElementById("bigcityLTEsudo").innerHTML = " 수도권 " + bigcityLTEsudo;
    
} else {
    document.getElementById("bigcityLTEsudo").innerHTML = "";
}



if (smallcityLTEseoul > 0) {
    document.getElementById("smallcityLTEseoul").innerHTML = " 서울 " + smallcityLTEseoul;
    
} else {
    document.getElementById("smallcityLTEseoul").innerHTML = "";
}
if (smallcityLTEincheon > 0) {
    document.getElementById("smallcityLTEincheon").innerHTML = " 인천 " + smallcityLTEincheon;
    
} else {
    document.getElementById("smallcityLTEincheon").innerHTML = "";
}
if (smallcityLTEulsan > 0) {
    document.getElementById("smallcityLTEulsan").innerHTML = " 울산 " + smallcityLTEulsan;
    
} else {
    document.getElementById("smallcityLTEulsan").innerHTML = "";
}
if (smallcityLTEdaegu > 0) {
    document.getElementById("smallcityLTEdaegu").innerHTML = " 대구 " + smallcityLTEdaegu;
    
} else {
    document.getElementById("smallcityLTEdaegu").innerHTML = "";
}
if (smallcityLTEgwangju > 0) {
    document.getElementById("smallcityLTEgwangju").innerHTML = " 광주 " + smallcityLTEgwangju;
    
} else {
    document.getElementById("smallcityLTEgwangju").innerHTML = "";
}
if (smallcityLTEdaejun > 0) {
    document.getElementById("smallcityLTEdaejun").innerHTML = " 대전 " + smallcityLTEdaejun;
    
} else {
    document.getElementById("smallcityLTEdaejun").innerHTML = "";
}
if (smallcityLTEgyunggi > 0) {
    document.getElementById("smallcityLTEgyunggi").innerHTML = " 경기 " + smallcityLTEgyunggi;
    
} else {
    document.getElementById("smallcityLTEgyunggi").innerHTML = "";
}
if (smallcityLTEgyungbuk > 0) {
    document.getElementById("smallcityLTEgyungbuk").innerHTML = " 경북 " + smallcityLTEgyungbuk;
    
} else {
    document.getElementById("smallcityLTEgyungbuk").innerHTML = "";
}
if (smallcityLTEjunnam > 0) {
    document.getElementById("smallcityLTEjunnam").innerHTML = " 전남 " + smallcityLTEjunnam;
    
} else {
    document.getElementById("smallcityLTEjunnam").innerHTML = "";
}
if (smallcityLTEjunbuk > 0) {
    document.getElementById("smallcityLTEjunbuk").innerHTML = " 전북 " + smallcityLTEjunbuk;
    
} else {
    document.getElementById("smallcityLTEjunbuk").innerHTML = "";
}
if (smallcityLTEchungnam > 0) {
    document.getElementById("smallcityLTEchungnam").innerHTML = " 충남 " + smallcityLTEchungnam;
    
} else {
    document.getElementById("smallcityLTEchungnam").innerHTML = "";
}
if (smallcityLTEchungbuk > 0) {
    document.getElementById("smallcityLTEchungbuk").innerHTML = " 충북 " + smallcityLTEchungbuk;
    
} else {
    document.getElementById("smallcityLTEchungbuk").innerHTML = "";
}
if (smallcityLTEsejong > 0) {
    document.getElementById("smallcityLTEsejong").innerHTML = " 세종 " + smallcityLTEsejong;
    
} else {
    document.getElementById("smallcityLTEsejong").innerHTML = "";
}
if (smallcityLTEsudo > 0) {
    document.getElementById("smallcityLTEsudo").innerHTML = " 수도권 " + smallcityLTEsudo;
    
} else {
    document.getElementById("smallcityLTEsudo").innerHTML = "";
}


if (nongLTEseoul > 0) {
    document.getElementById("nongLTEseoul").innerHTML = " 서울 " + nongLTEseoul;
    
} else {
    document.getElementById("nongLTEseoul").innerHTML = "";
}
if (nongLTEincheon > 0) {
    document.getElementById("nongLTEincheon").innerHTML = " 인천 " + nongLTEincheon;
    
} else {
    document.getElementById("nongLTEincheon").innerHTML = "";
}
if (nongLTEulsan > 0) {
    document.getElementById("nongLTEulsan").innerHTML = " 울산 " + nongLTEulsan;
    
} else {
    document.getElementById("nongLTEulsan").innerHTML = "";
}
if (nongLTEdaegu > 0) {
    document.getElementById("nongLTEdaegu").innerHTML = " 대구 " + nongLTEdaegu;
    
} else {
    document.getElementById("nongLTEdaegu").innerHTML = "";
}
if (nongLTEgwangju > 0) {
    document.getElementById("nongLTEgwangju").innerHTML = " 광주 " + nongLTEgwangju;
    
} else {
    document.getElementById("nongLTEgwangju").innerHTML = "";
}
if (nongLTEdaejun > 0) {
    document.getElementById("nongLTEdaejun").innerHTML = " 대전 " + nongLTEdaejun;
    
} else {
    document.getElementById("nongLTEdaejun").innerHTML = "";
}
if (nongLTEgyunggi > 0) {
    document.getElementById("nongLTEgyunggi").innerHTML = " 경기 " + nongLTEgyunggi;
    
} else {
    document.getElementById("nongLTEgyunggi").innerHTML = "";
}
if (nongLTEgyungbuk > 0) {
    document.getElementById("nongLTEgyungbuk").innerHTML = " 경북 " + nongLTEgyungbuk;
    
} else {
    document.getElementById("nongLTEgyungbuk").innerHTML = "";
}
if (nongLTEjunnam > 0) {
    document.getElementById("nongLTEjunnam").innerHTML = " 전남 " + nongLTEjunnam;
    
} else {
    document.getElementById("nongLTEjunnam").innerHTML = "";
}
if (nongLTEjunbuk > 0) {
    document.getElementById("nongLTEjunbuk").innerHTML = " 전북 " + nongLTEjunbuk;
    
} else {
    document.getElementById("nongLTEjunbuk").innerHTML = "";
}
if (nongLTEchungnam > 0) {
    document.getElementById("nongLTEchungnam").innerHTML = " 충남 " + nongLTEchungnam;
    
} else {
    document.getElementById("nongLTEchungnam").innerHTML = "";
}
if (nongLTEchungbuk > 0) {
    document.getElementById("nongLTEchungbuk").innerHTML = " 충북 " + nongLTEchungbuk;
    
} else {
    document.getElementById("nongLTEchungbuk").innerHTML = "";
}
if (nongLTEsejong > 0) {
    document.getElementById("nongLTEsejong").innerHTML = " 세종 " + nongLTEsejong;
    
} else {
    document.getElementById("nongLTEsejong").innerHTML = "";
}
if (nongLTEsudo > 0) {
    document.getElementById("nongLTEsudo").innerHTML = " 수도권 " + nongLTEsudo;
    
} else {
    document.getElementById("nongLTEsudo").innerHTML = "";
}


if (inbuildingLTEcdys > 0) {
    document.getElementById("inbuildingLTEcdys").innerHTML = " 철도역사 " + inbuildingLTEcdys;
    
} else {
    document.getElementById("inbuildingLTEcdys").innerHTML = "";

}if (inbuildingLTEdhbw > 0) {
    document.getElementById("inbuildingLTEdhbw").innerHTML = " 대형병원 " + inbuildingLTEdhbw;
    
} else {
    document.getElementById("inbuildingLTEdhbw").innerHTML = "";

}if (inbuildingLTEbhj > 0) {
    document.getElementById("inbuildingLTEbhj").innerHTML = " 백화점 " + inbuildingLTEbhj;
    
} else {
    document.getElementById("inbuildingLTEbhj").innerHTML = "";

}if (inbuildingLTEtmn > 0) {
    document.getElementById("inbuildingLTEtmn").innerHTML = " 터미널 " + inbuildingLTEtmn;
    
} else {
    document.getElementById("inbuildingLTEtmn").innerHTML = "";
    
}if (inbuildingLTEgh > 0) {
    document.getElementById("inbuildingLTEgh").innerHTML = " 공항 " + inbuildingLTEgh;
    
} else {
    document.getElementById("inbuildingLTEgh").innerHTML = "";
    
   }   if (inbuildingLTEdhjp > 0) {
    document.getElementById("inbuildingLTEdhjp").innerHTML = " 대형점포 " + inbuildingLTEdhjp;
    
} else {
    document.getElementById("inbuildingLTEdhjp").innerHTML = "";
    
}if (inbuildingLTEjsj > 0) {
    document.getElementById("inbuildingLTEjsj").innerHTML = " 전시장 " + inbuildingLTEjsj;
    
} else {
    document.getElementById("inbuildingLTEjsj").innerHTML = "";

   }   if (inbuildingLTEjhcys > 0) {
    document.getElementById("inbuildingLTEjhcys").innerHTML = " 지하철역사 " + inbuildingLTEjhcys;
    
} else {
    document.getElementById("inbuildingLTEjhcys").innerHTML = "";

}if (themeLTEjunnam > 0) {
        document.getElementById("themeLTEjunnam").innerHTML = " 대학교 " + themeLTEjunnam;
        
} else {
        document.getElementById("themeLTEjunnam").innerHTML = "";

       }       if (themeLTEjunbuk > 0) {
    document.getElementById("themeLTEjunbuk").innerHTML = " 놀이공원 " + themeLTEjunbuk;
    
} else {
    document.getElementById("themeLTEjunbuk").innerHTML = "";

}
if (themeLTEchungnam > 0) {
        document.getElementById("themeLTEchungnam").innerHTML = " 주요거리 " + themeLTEchungnam;
        
} else {
        document.getElementById("themeLTEchungnam").innerHTML = "";

}if (themeLTEchungbuk > 0) {
    document.getElementById("themeLTEchungbuk").innerHTML = " 전통시장 " + themeLTEchungbuk;
    
} else {
    document.getElementById("themeLTEchungbuk").innerHTML = "";

}if (themeLTEsejong > 0) {
    document.getElementById("themeLTEsejong").innerHTML = " 지하철노선 " + themeLTEsejong;
    
} else {
    document.getElementById("themeLTEsejong").innerHTML = "";
}

// 리포트 날짜
date = new Date();
year = date.getFullYear();
month = date.getMonth() + 1;
day = date.getDate();
document.getElementById("current_date").innerHTML = month + "."
        + day + "." + year;

var date1 =  document.getElementById("firstdate").outerText;
date1 = date1.substr(6);
document.getElementById("firstdate").innerText = "(" + date1 + "~";

var date2 = document.getElementById("lastdate").outerText;
date2 = date2.substr(6);
document.getElementById("lastdate").innerHTML = date2 + ")";
