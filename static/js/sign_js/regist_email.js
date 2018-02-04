/**
 * Created by Suyn on 2018/1/25.
 */
//获取cookie
function get_cookie(name) {
    var xsrf_cookies = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return xsrf_cookies[1];
}

//提交登录请求
$(document).ready(function(){
    $('#email_code_submit').click(function (event) {
        event.preventDefault();
        $.ajax({
            'url': '/email_code',
            'type': 'post',
            'data': {
               'email_code': $('#email').val(),
               'email_num': $('#email_num').val(),
            },
            'headers':{
                 "X-XSRFTOKEN":get_cookie("_xsrf")
            },
            'success': function (data) {
                var error = document.getElementById('error');
               if(data['status'] == 200){
                   error.innerHTML = '<div class="alert alert-success" role="alert">'+data['msg']+'</div>';
                   setTimeout(function(){window.location = '/login';},1000);
               }else {

                   error.innerHTML = '<div class="alert alert-success" role="alert">'+data['msg']+'</div>';
               }
            }
        });
    });
});