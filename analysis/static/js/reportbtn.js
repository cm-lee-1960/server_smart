// 일일보고 수정
	function printName1() {
		const textmod = document.getElementById('textmod1').value;
		document.getElementById("result1").innerText = textmod;
	}
	function printName2() {
		const textmod = document.getElementById('textmod2').value;
		document.getElementById("result2").innerText = textmod;
	}
	function printName3() {
		const textmod = document.getElementById('textmod3').value;
		document.getElementById("result3").innerText = textmod;
	}
	function printName4() {
		const textmod = document.getElementById('textmod4').value;
		document.getElementById("result4").innerText = textmod;
	}


// 수정 완료 이벤트
		$("#textmod1").hide();
		$("#textmod2").hide();
		$("#textmod3").hide();
		$("#textmod4").hide();

		$('#modify').click(function() {

			$("#textmod1").show();
			$("#textmod2").show();
			$("#textmod3").show();
			$("#textmod4").show();
		});
		$('#complete').click(function() {

			$("#textmod1").hide();
			$("#textmod2").hide();
			$("#textmod3").hide();
			$("#textmod4").hide();
		});
	

// PDF 출력 버튼 이벤트
		$('#cmd').click(
				function() {
					var doc = new jsPDF();
					var specialElementHandlers = {
						'#editor' : function(element, renderer) {
							return true;
						}
					};
					html2canvas($('#content'), {

						onrendered : function(canvas) {
							var imgData = canvas.toDataURL('jpeg');
							var imgWidth = 210; // 이미지 가로 길이(mm) A4 기준
							var pageHeight = imgWidth * 1.414; // 출력 페이지 세로 길이 계산 A4 기준
							var imgHeight = canvas.height * imgWidth / canvas.width;
							var heightLeft = imgHeight;
							var margin = 20; // 출력 페이지 여백설정
							var position = 10;
							var doc = new jsPDF("p", "mm");

							doc.addImage(imgData, 'JPEG', margin, position, imgWidth, imgHeight);
							heightLeft -= pageHeight;
							// 한 페이지 이상일 경우 루프 돌면서 출력
							while (heightLeft >= 0) {
								position += heightLeft - imgHeight;
								doc.addPage();
								doc.addImage(imgData, 'JPEG', margin, position, imgWidth, imgHeight);
								heightLeft -= pageHeight;
							}
							doc.save('test.pdf');

						}
					});
				});
	