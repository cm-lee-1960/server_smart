
//그래프 퍼센트 데이터
var plan5g1 = parseInt(document.getElementById("plan5g1").outerText);
var plan5g2 = parseInt(document.getElementById("plan5g2").outerText);
var plan5g3 = parseInt(document.getElementById("plan5g3").outerText);
var plan5g4 = parseInt(document.getElementById("plan5g4").outerText);
var plan5g5 = parseInt(document.getElementById("plan5g5").outerText);
var plan5g6 = parseInt(document.getElementById("plan5g6").outerText);
var plan5g7 = parseInt(document.getElementById("plan5g7").outerText);
var planarea4 = parseInt(document.getElementById("planarea4").outerText);
var planarea5 = parseInt(document.getElementById("planarea5").outerText);
var planarea6 = parseInt(document.getElementById("planarea6").outerText);
var planarea7 = parseInt(document.getElementById("planarea7").outerText);
var planarea8 = parseInt(document.getElementById("planarea8").outerText);
var planarea9 = parseInt(document.getElementById("planarea9").outerText);
var planarea10 = parseInt(document.getElementById("planarea10").outerText);
var planarea11 = parseInt(document.getElementById("planarea11").outerText);
var planarea12 = parseInt(document.getElementById("planarea12").outerText);
var planarea13 = parseInt(document.getElementById("planarea13").outerText);
var planarea14 = parseInt(document.getElementById("planarea14").outerText);
var planarea15 = parseInt(document.getElementById("planarea15").outerText);
var result5g1 = parseInt(document.getElementById("result5g1").outerText);
var result5g2 = parseInt(document.getElementById("result5g2").outerText);
var result5g3 = parseInt(document.getElementById("result5g3").outerText);
var result5g4 = parseInt(document.getElementById("result5g4").outerText);
var result5g5 = parseInt(document.getElementById("result5g5").outerText);
var result5g6 = parseInt(document.getElementById("result5g6").outerText);
var result5g7 = parseInt(document.getElementById("result5g7").outerText);
var resultarea4 = parseInt(document.getElementById("resultarea4").outerText);
var resultarea5 = parseInt(document.getElementById("resultarea5").outerText);
var resultarea6 = parseInt(document.getElementById("resultarea6").outerText);
var resultarea7 = parseInt(document.getElementById("resultarea7").outerText);
var resultarea8 = parseInt(document.getElementById("resultarea8").outerText);
var resultarea9 = parseInt(document.getElementById("resultarea9").outerText);
var resultarea10 = parseInt(document.getElementById("resultarea10").outerText);
var resultarea11 = parseInt(document.getElementById("resultarea11").outerText);
var resultarea12 = parseInt(document.getElementById("resultarea12").outerText);
var resultarea13 = parseInt(document.getElementById("resultarea13").outerText);
var resultarea14 = parseInt(document.getElementById("resultarea14").outerText);
var resultarea15 = parseInt(document.getElementById("resultarea15").outerText);

document.getElementById("result5g1").innerHTML = result5g1+"("+((result5g1/plan5g1)*100).toFixed(0)+"%)";
document.getElementById("result5g2").innerHTML = result5g2+"("+((result5g2/plan5g2)*100).toFixed(0)+"%)";
document.getElementById("result5g3").innerHTML = result5g3+"("+((result5g3/plan5g3)*100).toFixed(0)+"%)";
document.getElementById("result5g4").innerHTML = result5g4+"("+((result5g4/plan5g4)*100).toFixed(0)+"%)";
document.getElementById("result5g5").innerHTML = result5g5+"("+((result5g5/plan5g5)*100).toFixed(0)+"%)";
document.getElementById("result5g6").innerHTML = result5g6+"("+((result5g6/plan5g6)*100).toFixed(0)+"%)";
document.getElementById("result5g7").innerHTML = result5g7+"("+((result5g7/plan5g7)*100).toFixed(0)+"%)";
document.getElementById("resultarea4").innerHTML = resultarea4+"("+((resultarea4/planarea4)*100).toFixed(0)+"%)";
document.getElementById("resultarea5").innerHTML = resultarea5+"("+((resultarea5/planarea5)*100).toFixed(0)+"%)";
document.getElementById("resultarea6").innerHTML = resultarea6+"("+((resultarea6/planarea6)*100).toFixed(0)+"%)";
document.getElementById("resultarea7").innerHTML = resultarea7+"("+((resultarea7/planarea7)*100).toFixed(0)+"%)";
document.getElementById("resultarea8").innerHTML = resultarea8+"("+((resultarea8/planarea8)*100).toFixed(0)+"%)";
document.getElementById("resultarea9").innerHTML = resultarea9+"("+((resultarea9/planarea9)*100).toFixed(0)+"%)";
document.getElementById("resultarea10").innerHTML = resultarea10+"("+((resultarea10/planarea10)*100).toFixed(0)+"%)";
document.getElementById("resultarea11").innerHTML = resultarea11+"("+((resultarea11/planarea11)*100).toFixed(0)+"%)";
document.getElementById("resultarea12").innerHTML = resultarea12+"("+((resultarea12/planarea12)*100).toFixed(0)+"%)";
document.getElementById("resultarea13").innerHTML = resultarea13+"("+((resultarea13/planarea13)*100).toFixed(0)+"%)";
document.getElementById("resultarea14").innerHTML = resultarea14+"("+((resultarea14/planarea14)*100).toFixed(0)+"%)";
document.getElementById("resultarea15").innerHTML = resultarea15+"("+((resultarea15/planarea15)*100).toFixed(0)+"%)";









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
document.getElementById("pcf").innerHTML = "(진도율:" + (((total5+total6+total7+total8)/(total1+total2+total3+total4))*100).toFixed(0) + "%)";


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


//와이파이 지역별 숫자 설정
var sangWiFiseoul=parseInt(document.getElementById('sangWiFiseoul').outerText);
var sangWiFiincheon=parseInt(document.getElementById('sangWiFiincheon').outerText);
var sangWiFiulsan=parseInt(document.getElementById('sangWiFiulsan').outerText);
var sangWiFidaegu=parseInt(document.getElementById('sangWiFidaegu').outerText);
var sangWiFigwangju=parseInt(document.getElementById('sangWiFigwangju').outerText);
var sangWiFidaejun=parseInt(document.getElementById('sangWiFidaejun').outerText);
var sangWiFigyunggi=parseInt(document.getElementById('sangWiFigyunggi').outerText);
var sangWiFigyungbuk=parseInt(document.getElementById('sangWiFigyungbuk').outerText);
var sangWiFijunnam=parseInt(document.getElementById('sangWiFijunnam').outerText);
var sangWiFijunbuk=parseInt(document.getElementById('sangWiFijunbuk').outerText);
var sangWiFichungnam=parseInt(document.getElementById('sangWiFichungnam').outerText);
var sangWiFichungbuk=parseInt(document.getElementById('sangWiFichungbuk').outerText);
var sangWiFisejong=parseInt(document.getElementById('sangWiFisejong').outerText);
var sangWiFisudo=parseInt(document.getElementById('sangWiFisudo').outerText);
var gaeWiFiseoul=parseInt(document.getElementById('gaeWiFiseoul').outerText);
var gaeWiFiincheon=parseInt(document.getElementById('gaeWiFiincheon').outerText);
var gaeWiFiulsan=parseInt(document.getElementById('gaeWiFiulsan').outerText);
var gaeWiFidaegu=parseInt(document.getElementById('gaeWiFidaegu').outerText);
var gaeWiFigwangju=parseInt(document.getElementById('gaeWiFigwangju').outerText);
var gaeWiFidaejun=parseInt(document.getElementById('gaeWiFidaejun').outerText);
var gaeWiFigyunggi=parseInt(document.getElementById('gaeWiFigyunggi').outerText);
var gaeWiFigyungbuk=parseInt(document.getElementById('gaeWiFigyungbuk').outerText);
var gaeWiFijunnam=parseInt(document.getElementById('gaeWiFijunnam').outerText);
var gaeWiFijunbuk=parseInt(document.getElementById('gaeWiFijunbuk').outerText);
var gaeWiFichungnam=parseInt(document.getElementById('gaeWiFichungnam').outerText);
var gaeWiFichungbuk=parseInt(document.getElementById('gaeWiFichungbuk').outerText);
var gaeWiFisejong=parseInt(document.getElementById('gaeWiFisejong').outerText);
var gaeWiFisudo=parseInt(document.getElementById('gaeWiFisudo').outerText);
var trainsangWiFiseoul=parseInt(document.getElementById('trainsangWiFiseoul').outerText);
var trainsangWiFiincheon=parseInt(document.getElementById('trainsangWiFiincheon').outerText);
var trainsangWiFiulsan=parseInt(document.getElementById('trainsangWiFiulsan').outerText);
var trainsangWiFidaegu=parseInt(document.getElementById('trainsangWiFidaegu').outerText);
var trainsangWiFigwangju=parseInt(document.getElementById('trainsangWiFigwangju').outerText);
var trainsangWiFidaejun=parseInt(document.getElementById('trainsangWiFidaejun').outerText);
var trainsangWiFigyunggi=parseInt(document.getElementById('trainsangWiFigyunggi').outerText);
var trainsangWiFigyungbuk=parseInt(document.getElementById('trainsangWiFigyungbuk').outerText);
var trainsangWiFijunnam=parseInt(document.getElementById('trainsangWiFijunnam').outerText);
var trainsangWiFijunbuk=parseInt(document.getElementById('trainsangWiFijunbuk').outerText);
var trainsangWiFichungnam=parseInt(document.getElementById('trainsangWiFichungnam').outerText);
var trainsangWiFichungbuk=parseInt(document.getElementById('trainsangWiFichungbuk').outerText);
var trainsangWiFisejong=parseInt(document.getElementById('trainsangWiFisejong').outerText);
var trainsangWiFisudo=parseInt(document.getElementById('trainsangWiFisudo').outerText);
var traingaeWiFiseoul=parseInt(document.getElementById('traingaeWiFiseoul').outerText);
var traingaeWiFiincheon=parseInt(document.getElementById('traingaeWiFiincheon').outerText);
var traingaeWiFiulsan=parseInt(document.getElementById('traingaeWiFiulsan').outerText);
var traingaeWiFidaegu=parseInt(document.getElementById('traingaeWiFidaegu').outerText);
var traingaeWiFigwangju=parseInt(document.getElementById('traingaeWiFigwangju').outerText);
var traingaeWiFidaejun=parseInt(document.getElementById('traingaeWiFidaejun').outerText);
var traingaeWiFigyunggi=parseInt(document.getElementById('traingaeWiFigyunggi').outerText);
var traingaeWiFigyungbuk=parseInt(document.getElementById('traingaeWiFigyungbuk').outerText);
var traingaeWiFijunnam=parseInt(document.getElementById('traingaeWiFijunnam').outerText);
var traingaeWiFijunbuk=parseInt(document.getElementById('traingaeWiFijunbuk').outerText);
var traingaeWiFichungnam=parseInt(document.getElementById('traingaeWiFichungnam').outerText);
var traingaeWiFichungbuk=parseInt(document.getElementById('traingaeWiFichungbuk').outerText);
var traingaeWiFisejong=parseInt(document.getElementById('traingaeWiFisejong').outerText);
var traingaeWiFisudo=parseInt(document.getElementById('traingaeWiFisudo').outerText);
var trainWiFisangtotal= trainsangWiFiseoul+trainsangWiFiincheon+trainsangWiFiulsan+trainsangWiFidaegu+trainsangWiFigwangju+trainsangWiFidaejun+trainsangWiFigyunggi+trainsangWiFigyungbuk+trainsangWiFijunnam+trainsangWiFijunbuk+trainsangWiFichungnam+trainsangWiFichungbuk+trainsangWiFisejong+trainsangWiFisudo;
var trainWiFigaetotal= traingaeWiFiseoul+traingaeWiFiincheon+traingaeWiFiulsan+traingaeWiFidaegu+traingaeWiFigwangju+traingaeWiFidaejun+traingaeWiFigyunggi+traingaeWiFigyungbuk+traingaeWiFijunnam+traingaeWiFijunbuk+traingaeWiFichungnam+traingaeWiFichungbuk+traingaeWiFisejong+traingaeWiFisudo;

//상용와이파이 개수(지하철X)
if (sangWiFiseoul > 0) {
    document.getElementById("sangWiFiseoul").innerHTML = " 서울 " + sangWiFiseoul;
    
} else {
    document.getElementById("sangWiFiseoul").innerHTML = "";
}
if (sangWiFiincheon > 0) {
    document.getElementById("sangWiFiincheon").innerHTML = " 인천 " + sangWiFiincheon;
    
} else {
    document.getElementById("sangWiFiincheon").innerHTML = "";
}
if (sangWiFiulsan > 0) {
    document.getElementById("sangWiFiulsan").innerHTML = " 울산 " + sangWiFiulsan;
    
} else {
    document.getElementById("sangWiFiulsan").innerHTML = "";
}
if (sangWiFidaegu > 0) {
    document.getElementById("sangWiFidaegu").innerHTML = " 대구 " + sangWiFidaegu;
    
} else {
    document.getElementById("sangWiFidaegu").innerHTML = "";
}
if (sangWiFigwangju > 0) {
    document.getElementById("sangWiFigwangju").innerHTML = " 광주 " + sangWiFigwangju;
    
} else {
    document.getElementById("sangWiFigwangju").innerHTML = "";
}
if (sangWiFidaejun > 0) {
    document.getElementById("sangWiFidaejun").innerHTML = " 대전 " + sangWiFidaejun;
    
} else {
    document.getElementById("sangWiFidaejun").innerHTML = "";
}
if (sangWiFigyunggi > 0) {
    document.getElementById("sangWiFigyunggi").innerHTML = " 경기 " + sangWiFigyunggi;
    
} else {
    document.getElementById("sangWiFigyunggi").innerHTML = "";
}
if (sangWiFigyungbuk > 0) {
    document.getElementById("sangWiFigyungbuk").innerHTML = " 경북 " + sangWiFigyungbuk;
    
} else {
    document.getElementById("sangWiFigyungbuk").innerHTML = "";
}
if (sangWiFijunnam > 0) {
    document.getElementById("sangWiFijunnam").innerHTML = " 전남 " + sangWiFijunnam;
    
} else {
    document.getElementById("sangWiFijunnam").innerHTML = "";
}
if (sangWiFijunbuk > 0) {
    document.getElementById("sangWiFijunbuk").innerHTML = " 전북 " + sangWiFijunbuk;
    
} else {
    document.getElementById("sangWiFijunbuk").innerHTML = "";
}
if (sangWiFichungnam > 0) {
    document.getElementById("sangWiFichungnam").innerHTML = " 충남 " + sangWiFichungnam;
    
} else {
    document.getElementById("sangWiFichungnam").innerHTML = "";
}
if (sangWiFichungbuk > 0) {
    document.getElementById("sangWiFichungbuk").innerHTML = " 충북 " + sangWiFichungbuk;
    
} else {
    document.getElementById("sangWiFichungbuk").innerHTML = "";
}
if (sangWiFisejong > 0) {
    document.getElementById("sangWiFisejong").innerHTML = " 세종 " + sangWiFisejong;
    
} else {
    document.getElementById("sangWiFisejong").innerHTML = "";
}
if (sangWiFisudo > 0) {
    document.getElementById("sangWiFisudo").innerHTML = " 수도권 " + sangWiFisudo;
    
} else {
    document.getElementById("sangWiFisudo").innerHTML = "";
}

//상용와이파이 개수 (지하철)

if (trainWiFisangtotal > 0) {
    document.getElementById("trainWiFisangtotal").innerHTML = " 지하철 " + trainWiFisangtotal;
    
} else {
    document.getElementById("trainWiFisangtotal").innerHTML = "";
}

if (trainsangWiFiseoul > 0) {
    document.getElementById("trainsangWiFiseoul").innerHTML = " 서울 " + trainsangWiFiseoul;
    
} else {
    document.getElementById("trainsangWiFiseoul").innerHTML = "";
}
if (trainsangWiFiincheon > 0) {
    document.getElementById("trainsangWiFiincheon").innerHTML = " 인천 " + trainsangWiFiincheon;
    
} else {
    document.getElementById("trainsangWiFiincheon").innerHTML = "";
}
if (trainsangWiFiulsan > 0) {
    document.getElementById("trainsangWiFiulsan").innerHTML = " 울산 " + trainsangWiFiulsan;
    
} else {
    document.getElementById("trainsangWiFiulsan").innerHTML = "";
}
if (trainsangWiFidaegu > 0) {
    document.getElementById("trainsangWiFidaegu").innerHTML = " 대구 " + trainsangWiFidaegu;
    
} else {
    document.getElementById("trainsangWiFidaegu").innerHTML = "";
}
if (trainsangWiFigwangju > 0) {
    document.getElementById("trainsangWiFigwangju").innerHTML = " 광주 " + trainsangWiFigwangju;
    
} else {
    document.getElementById("trainsangWiFigwangju").innerHTML = "";
}
if (trainsangWiFidaejun > 0) {
    document.getElementById("trainsangWiFidaejun").innerHTML = " 대전 " + trainsangWiFidaejun;
    
} else {
    document.getElementById("trainsangWiFidaejun").innerHTML = "";
}
if (trainsangWiFigyunggi > 0) {
    document.getElementById("trainsangWiFigyunggi").innerHTML = " 경기 " + trainsangWiFigyunggi;
    
} else {
    document.getElementById("trainsangWiFigyunggi").innerHTML = "";
}
if (trainsangWiFigyungbuk > 0) {
    document.getElementById("trainsangWiFigyungbuk").innerHTML = " 경북 " + trainsangWiFigyungbuk;
    
} else {
    document.getElementById("trainsangWiFigyungbuk").innerHTML = "";
}
if (trainsangWiFijunnam > 0) {
    document.getElementById("trainsangWiFijunnam").innerHTML = " 전남 " + trainsangWiFijunnam;
    
} else {
    document.getElementById("trainsangWiFijunnam").innerHTML = "";
}
if (trainsangWiFijunbuk > 0) {
    document.getElementById("trainsangWiFijunbuk").innerHTML = " 전북 " + trainsangWiFijunbuk;
    
} else {
    document.getElementById("trainsangWiFijunbuk").innerHTML = "";
}
if (trainsangWiFichungnam > 0) {
    document.getElementById("trainsangWiFichungnam").innerHTML = " 충남 " + trainsangWiFichungnam;
    
} else {
    document.getElementById("trainsangWiFichungnam").innerHTML = "";
}
if (trainsangWiFichungbuk > 0) {
    document.getElementById("trainsangWiFichungbuk").innerHTML = " 충북 " + trainsangWiFichungbuk;
    
} else {
    document.getElementById("trainsangWiFichungbuk").innerHTML = "";
}
if (trainsangWiFisejong > 0) {
    document.getElementById("trainsangWiFisejong").innerHTML = " 세종 " + trainsangWiFisejong;
    
} else {
    document.getElementById("trainsangWiFisejong").innerHTML = "";
}
if (trainsangWiFisudo > 0) {
    document.getElementById("trainsangWiFisudo").innerHTML = " 수도권 " + trainsangWiFisudo;
    
} else {
    document.getElementById("trainsangWiFisudo").innerHTML = "";
}
//개방와이파이 개수(지하철X)
if (gaeWiFiseoul > 0) {
    document.getElementById("gaeWiFiseoul").innerHTML = " 서울 " + gaeWiFiseoul;
    
} else {
    document.getElementById("gaeWiFiseoul").innerHTML = "";
}
if (gaeWiFiincheon > 0) {
    document.getElementById("gaeWiFiincheon").innerHTML = " 인천 " + gaeWiFiincheon;
    
} else {
    document.getElementById("gaeWiFiincheon").innerHTML = "";
}
if (gaeWiFiulsan > 0) {
    document.getElementById("gaeWiFiulsan").innerHTML = " 울산 " + gaeWiFiulsan;
    
} else {
    document.getElementById("gaeWiFiulsan").innerHTML = "";
}
if (gaeWiFidaegu > 0) {
    document.getElementById("gaeWiFidaegu").innerHTML = " 대구 " + gaeWiFidaegu;
    
} else {
    document.getElementById("gaeWiFidaegu").innerHTML = "";
}
if (gaeWiFigwangju > 0) {
    document.getElementById("gaeWiFigwangju").innerHTML = " 광주 " + gaeWiFigwangju;
    
} else {
    document.getElementById("gaeWiFigwangju").innerHTML = "";
}
if (gaeWiFidaejun > 0) {
    document.getElementById("gaeWiFidaejun").innerHTML = " 대전 " + gaeWiFidaejun;
    
} else {
    document.getElementById("gaeWiFidaejun").innerHTML = "";
}
if (gaeWiFigyunggi > 0) {
    document.getElementById("gaeWiFigyunggi").innerHTML = " 경기 " + gaeWiFigyunggi;
    
} else {
    document.getElementById("gaeWiFigyunggi").innerHTML = "";
}
if (gaeWiFigyungbuk > 0) {
    document.getElementById("gaeWiFigyungbuk").innerHTML = " 경북 " + gaeWiFigyungbuk;
    
} else {
    document.getElementById("gaeWiFigyungbuk").innerHTML = "";
}
if (gaeWiFijunnam > 0) {
    document.getElementById("gaeWiFijunnam").innerHTML = " 전남 " + gaeWiFijunnam;
    
} else {
    document.getElementById("gaeWiFijunnam").innerHTML = "";
}
if (gaeWiFijunbuk > 0) {
    document.getElementById("gaeWiFijunbuk").innerHTML = " 전북 " + gaeWiFijunbuk;
    
} else {
    document.getElementById("gaeWiFijunbuk").innerHTML = "";
}
if (gaeWiFichungnam > 0) {
    document.getElementById("gaeWiFichungnam").innerHTML = " 충남 " + gaeWiFichungnam;
    
} else {
    document.getElementById("gaeWiFichungnam").innerHTML = "";
}
if (gaeWiFichungbuk > 0) {
    document.getElementById("gaeWiFichungbuk").innerHTML = " 충북 " + gaeWiFichungbuk;
    
} else {
    document.getElementById("gaeWiFichungbuk").innerHTML = "";
}
if (gaeWiFisejong > 0) {
    document.getElementById("gaeWiFisejong").innerHTML = " 세종 " + gaeWiFisejong;
    
} else {
    document.getElementById("gaeWiFisejong").innerHTML = "";
}
if (gaeWiFisudo > 0) {
    document.getElementById("gaeWiFisudo").innerHTML = " 수도권 " + gaeWiFisudo;
    
} else {
    document.getElementById("gaeWiFisudo").innerHTML = "";
}

//개방와이파이 개수 (지하철)
if (trainWiFigaetotal > 0) {
    document.getElementById("trainWiFigaetotal").innerHTML = " 지하철 " + trainWiFigaetotal;
    
} else {
    document.getElementById("trainWiFigaetotal").innerHTML = "";
}

if (traingaeWiFiseoul > 0) {
    document.getElementById("traingaeWiFiseoul").innerHTML = " 서울 " + traingaeWiFiseoul;
    
} else {
    document.getElementById("traingaeWiFiseoul").innerHTML = "";
}
if (traingaeWiFiincheon > 0) {
    document.getElementById("traingaeWiFiincheon").innerHTML = " 인천 " + traingaeWiFiincheon;
    
} else {
    document.getElementById("traingaeWiFiincheon").innerHTML = "";
}
if (traingaeWiFiulsan > 0) {
    document.getElementById("traingaeWiFiulsan").innerHTML = " 울산 " + traingaeWiFiulsan;
    
} else {
    document.getElementById("traingaeWiFiulsan").innerHTML = "";
}
if (traingaeWiFidaegu > 0) {
    document.getElementById("traingaeWiFidaegu").innerHTML = " 대구 " + traingaeWiFidaegu;
    
} else {
    document.getElementById("traingaeWiFidaegu").innerHTML = "";
}
if (traingaeWiFigwangju > 0) {
    document.getElementById("traingaeWiFigwangju").innerHTML = " 광주 " + traingaeWiFigwangju;
    
} else {
    document.getElementById("traingaeWiFigwangju").innerHTML = "";
}
if (traingaeWiFidaejun > 0) {
    document.getElementById("traingaeWiFidaejun").innerHTML = " 대전 " + traingaeWiFidaejun;
    
} else {
    document.getElementById("traingaeWiFidaejun").innerHTML = "";
}
if (traingaeWiFigyunggi > 0) {
    document.getElementById("traingaeWiFigyunggi").innerHTML = " 경기 " + traingaeWiFigyunggi;
    
} else {
    document.getElementById("traingaeWiFigyunggi").innerHTML = "";
}
if (traingaeWiFigyungbuk > 0) {
    document.getElementById("traingaeWiFigyungbuk").innerHTML = " 경북 " + traingaeWiFigyungbuk;
    
} else {
    document.getElementById("traingaeWiFigyungbuk").innerHTML = "";
}
if (traingaeWiFijunnam > 0) {
    document.getElementById("traingaeWiFijunnam").innerHTML = " 전남 " + traingaeWiFijunnam;
    
} else {
    document.getElementById("traingaeWiFijunnam").innerHTML = "";
}
if (traingaeWiFijunbuk > 0) {
    document.getElementById("traingaeWiFijunbuk").innerHTML = " 전북 " + traingaeWiFijunbuk;
    
} else {
    document.getElementById("traingaeWiFijunbuk").innerHTML = "";
}
if (traingaeWiFichungnam > 0) {
    document.getElementById("traingaeWiFichungnam").innerHTML = " 충남 " + traingaeWiFichungnam;
    
} else {
    document.getElementById("traingaeWiFichungnam").innerHTML = "";
}
if (traingaeWiFichungbuk > 0) {
    document.getElementById("traingaeWiFichungbuk").innerHTML = " 충북 " + traingaeWiFichungbuk;
    
} else {
    document.getElementById("traingaeWiFichungbuk").innerHTML = "";
}
if (traingaeWiFisejong > 0) {
    document.getElementById("traingaeWiFisejong").innerHTML = " 세종 " + traingaeWiFisejong;
    
} else {
    document.getElementById("traingaeWiFisejong").innerHTML = "";
}
if (traingaeWiFisudo > 0) {
    document.getElementById("traingaeWiFisudo").innerHTML = " 수도권 " + traingaeWiFisudo;
    
} else {
    document.getElementById("traingaeWiFisudo").innerHTML = "";
}






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
document.getElementById("current_date").innerHTML = year + "." + month + "." + day ;

let date1 = document.getElementById("firstdate").outerText;
date11 = String(date1);
year1 = date11.substr(0,4);
month1 = date11.substr(4,2);
day1 = date11.substr(6,2);
document.getElementById("firstdate").innerHTML = "(" + month1 + "." + day1 + "~";

let date2 = document.getElementById("lastdate").outerText;
date22 = String(date2);
year2 = date22.substr(0,4);
month2 = date22.substr(4,2);
day2 = date22.substr(6,2);
document.getElementById("lastdate").innerHTML = month2 + "." + day2 + ")";
