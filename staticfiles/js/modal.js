// <!-- 모달1 카테고리 변경에 따른 이벤트 -->

$(document).ready(function() {
    // $('#fst').hide();
    $('#scd').hide();
    $('#trd').hide();
    $('#fth').hide();
    $('#category').change(function() {
    var result = $('#category').val();
   
    if (result == '5G') {
        $('#fst').show();
        $('#scd').hide();
        $('#trd').hide();
        $('#fth').hide();
    } else if (result == 'LTE') {
        $('#fst').hide();
        $('#scd').show();
        $('#trd').hide();
        $('#fth').hide();
    } else if (result == 'WiFi') {
        $('#fst').hide();
        $('#scd').hide();
        $('#trd').show();
        $('#fth').hide();
    } else {
        $('#fst').hide();
        $('#scd').hide();
        $('#trd').hide();
        $('#fth').show();

        }
    }); 
}); 




{/* <!-- 모달2 카테고리 변경에 따른 이벤트 --> */}

$(document).ready(function() {
    // $('#5gdr').hide();
    $('#ltedr').hide();
    $('#wifidr').hide();
    $('#weakdr').hide();
    $('#category2').change(function() {
    var result = $('#category2').val();
   
    if (result == '5G') {
        $('#5gdr').show();
        $('#ltedr').hide();
        $('#wifidr').hide();
        $('#weakdr').hide();
    } else if (result == 'LTE') {
        $('#5gdr').hide();
        $('#ltedr').show();
        $('#wifidr').hide();
        $('#weakdr').hide();
    } else if (result == 'WiFi') {
        $('#5gdr').hide();
        $('#ltedr').hide();
        $('#wifidr').show();
        $('#weakdr').hide();
    } else {
        $('#5gdr').hide();
        $('#ltedr').hide();
        $('#wifidr').hide();
        $('#weakdr').show();

        }
    }); 
}); 

// <!-- 모달1자바스크립트 -->

    const modal = document.getElementById("modal")
    function modalOn() {
        modal.style.display = "flex"
    }
    function isModalOn() {
        return modal.style.display === "flex"
    }
    function modalOff() {
        modal.style.display = "none"
    }
    const btnModal = document.getElementById("dsdr")
    btnModal.addEventListener("click", e => {
        modalOn()
        modal2Off()
    })
    const closeBtn = modal.querySelector(".close-area")
    closeBtn.addEventListener("click", e => {
        modalOff()
    })
    modal.addEventListener("click", e => {
        const evTarget = e.target
        if(evTarget.classList.contains("modal-overlay")) {
            modalOff()
        }
    })
    window.addEventListener("keyup", e => {
        if(isModalOn() && e.key === "Escape") {
            modalOff()
        }
    })
   
    
    // <!-- 모달2자바스크립트 -->

    const modal2 = document.getElementById("modal2")
    function modal2On() {
        modal2.style.display = "flex"
    }
    function isModal2On() {
        return modal2.style.display === "flex"
    }
    function modal2Off() {
        modal2.style.display = "none"
    }
    const btnModal2 = document.getElementById("wrdr")
    btnModal2.addEventListener("click", e => {
        modal2On()
        modalOff()
    })
    const closeBtn2 = modal2.querySelector(".close-area")
    closeBtn2.addEventListener("click", e => {
        modal2Off()
    })
    modal2.addEventListener("click", e => {
        const evTarget2 = e.target
        if(evTarget2.classList.contains("modal-overlay")) {
            modal2Off()
        }
    })
    window.addEventListener("keyup", e => {
        if(isModal2On() && e.key === "Escape") {
            modal2Off()
        }
    })



    // <!-- 모달 이동 드래그 설정 -->
    
  
    $(function(){

        $('.modal-overlay').draggable({
            handle: ".top"
        });

        });
    // 드래그 가능 불가능 설정
    // $(function(){

    //     $('#pop_stop_info_detial').draggable({'cancel':'.tbl'});

    // });
    // 화면밖으로 나가는것 방지
    // $(function(){

    //     $('#modal-overlay').draggable({'cancel':'.tbl', containment:'parent', scroll:false});

    // });
 