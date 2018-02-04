
//获取cookie
function get_cookie(name) {
    var xsrf_cookies = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return xsrf_cookies[1]
}


//提交登录请求
$(document).ready(function(){
    $('#submit_danmu').click(function (event) {
        event.preventDefault();
        $.ajax({
            'url': '/congratulation',
            'type': 'post',
            'data': {
               'cong': $('#name').val(),
            },
            'headers':{
                 "X-XSRFTOKEN":get_cookie("_xsrf")
            },
            'success': function (data) {
               if(data['status'] == 200){
                   swal({
                    'title': '提交成功',
                    'text': data['msg'],
                    'type': 'success',
					'showCancelButton': false,
                    'showConfirmButton': false,
					'timer': 1500,
                    'closeOnConfirm': false
                    },function () {
                       window.location = '/';
                    });

               }else {
                    swal({
                    'title': '提交错误',
                    'text': data['msg'],
                    'type': 'error',
                    'showCancelButton': false,
                    'showConfirmButton': false,
                    'timer': 1500
                    });
                    get_image_code();
               }
            }
        });
    });
});

