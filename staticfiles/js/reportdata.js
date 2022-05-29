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

document.getElementById("result5g1").innerHTML =
  result5g1 + "(" + ((result5g1 / plan5g1) * 100).toFixed(0) + "%)";
document.getElementById("result5g2").innerHTML =
  result5g2 + "(" + ((result5g2 / plan5g2) * 100).toFixed(0) + "%)";
document.getElementById("result5g3").innerHTML =
  result5g3 + "(" + ((result5g3 / plan5g3) * 100).toFixed(0) + "%)";
document.getElementById("result5g4").innerHTML =
  result5g4 + "(" + ((result5g4 / plan5g4) * 100).toFixed(0) + "%)";
document.getElementById("result5g5").innerHTML =
  result5g5 + "(" + ((result5g5 / plan5g5) * 100).toFixed(0) + "%)";
document.getElementById("result5g6").innerHTML =
  result5g6 + "(" + ((result5g6 / plan5g6) * 100).toFixed(0) + "%)";
document.getElementById("result5g7").innerHTML =
  result5g7 + "(" + ((result5g7 / plan5g7) * 100).toFixed(0) + "%)";
document.getElementById("resultarea4").innerHTML =
  resultarea4 + "(" + ((resultarea4 / planarea4) * 100).toFixed(0) + "%)";
document.getElementById("resultarea5").innerHTML =
  resultarea5 + "(" + ((resultarea5 / planarea5) * 100).toFixed(0) + "%)";
document.getElementById("resultarea6").innerHTML =
  resultarea6 + "(" + ((resultarea6 / planarea6) * 100).toFixed(0) + "%)";
document.getElementById("resultarea7").innerHTML =
  resultarea7 + "(" + ((resultarea7 / planarea7) * 100).toFixed(0) + "%)";
document.getElementById("resultarea8").innerHTML =
  resultarea8 + "(" + ((resultarea8 / planarea8) * 100).toFixed(0) + "%)";
document.getElementById("resultarea9").innerHTML =
  resultarea9 + "(" + ((resultarea9 / planarea9) * 100).toFixed(0) + "%)";
document.getElementById("resultarea10").innerHTML =
  resultarea10 + "(" + ((resultarea10 / planarea10) * 100).toFixed(0) + "%)";
document.getElementById("resultarea11").innerHTML =
  resultarea11 + "(" + ((resultarea11 / planarea11) * 100).toFixed(0) + "%)";
document.getElementById("resultarea12").innerHTML =
  resultarea12 + "(" + ((resultarea12 / planarea12) * 100).toFixed(0) + "%)";
document.getElementById("resultarea13").innerHTML =
  resultarea13 + "(" + ((resultarea13 / planarea13) * 100).toFixed(0) + "%)";
document.getElementById("resultarea14").innerHTML =
  resultarea14 + "(" + ((resultarea14 / planarea14) * 100).toFixed(0) + "%)";
document.getElementById("resultarea15").innerHTML =
  resultarea15 + "(" + ((resultarea15 / planarea15) * 100).toFixed(0) + "%)";

// 리포트데이터 정제
var total1 = parseInt(document.getElementById("5tt").outerText);
var total2 = parseInt(document.getElementById("ltt").outerText);
var total3 = parseInt(document.getElementById("witt").outerText);
var total4 = parseInt(document.getElementById("wtt").outerText);
var total5 = parseInt(document.getElementById("5nj").outerText);
var total6 = parseInt(document.getElementById("lnj").outerText);
var total7 = parseInt(document.getElementById("winj").outerText);
var total8 = parseInt(document.getElementById("wnj").outerText);

document.getElementById("tt1").innerHTML = total1 + "개 지역 중";
document.getElementById("tt2").innerHTML = total2 + "개 지역 중";
document.getElementById("tt3").innerHTML = total3 + "개 지역 중";
document.getElementById("tt4").innerHTML = total4 + "개 지역 중";
document.getElementById("pc1").innerHTML =
  "(" + ((total5 / total1) * 100).toFixed(2) + "%)";
document.getElementById("pc2").innerHTML =
  "(" + ((total6 / total2) * 100).toFixed(2) + "%)";
document.getElementById("pc3").innerHTML =
  "(" + ((total7 / total3) * 100).toFixed(2) + "%)";
document.getElementById("pc4").innerHTML =
  "(" + ((total8 / total4) * 100).toFixed(2) + "%)";
document.getElementById("tt").innerHTML =
  total1 + total2 + total3 + total4 + "개";
document.getElementById("ttf").innerHTML =
  total5 + total6 + total7 + total8 + "개";
document.getElementById("pcf").innerHTML =
  "(진도율:" +
  (
    ((total5 + total6 + total7 + total8) /
      (total1 + total2 + total3 + total4)) *
    100
  ).toFixed(0) +
  "%)";

// 리포트 날짜
date = new Date();
year = date.getFullYear();
month = date.getMonth() + 1;
day = date.getDate();
document.getElementById("current_date").innerHTML =
  year + "." + month + "." + day;

let date1 = document.getElementById("firstdate").outerText;
date11 = String(date1);
year1 = date11.substr(0, 4);
month1 = date11.substr(4, 2);
day1 = date11.substr(6, 2);
document.getElementById("firstdate").innerHTML =
  "(" + month1 + "." + day1 + "~";

let date2 = document.getElementById("lastdate").outerText;
date22 = String(date2);
year2 = date22.substr(0, 4);
month2 = date22.substr(4, 2);
day2 = date22.substr(6, 2);
document.getElementById("lastdate").innerHTML = month2 + "." + day2 + ")";
