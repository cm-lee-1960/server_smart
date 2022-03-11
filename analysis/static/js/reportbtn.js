// 일일보고 수정
	function printName() {
		const name = document.getElementById('name').value;
		document.getElementById("result").innerText = name;
	}
	function printName1() {
		const name = document.getElementById('name1').value;
		document.getElementById("result1").innerText = name;
	}
	function printName2() {
		const name = document.getElementById('name2').value;
		document.getElementById("result2").innerText = name;
	}



// 수정 완료 이벤트
		$("#name").hide();
		$("#name1").hide();
		$("#name2").hide();

		$('#modify').click(function() {

			$("#name").show();
			$("#name1").show();
			$("#name2").show();

		});
		$('#complete').click(function() {

			$("#name").hide();
			$("#name1").hide();
			$("#name2").hide();

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
	