/**
 * Created by Suyn on 2017/11/29.
 */
//获取cookie
function get_cookie(name) {
    var xsrf_cookies = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return xsrf_cookies[1];
}

//提交登录请求
$(document).ready(function(){
    $('#found_submit').click(function (event) {
        event.preventDefault();
        $.ajax({
            'url': '/forget/found_password',
            'type': 'post',
            'data': {
               'e_mail': $('#e_mail').val(),
               'code': $('#code').val(),
               'password1':  $('#password1').val(),
               'password2':  $('#password2').val(),
            },
            'headers':{
                 "X-XSRFTOKEN":get_cookie("_xsrf")
            },
            'success': function (data) {
                var error = document.getElementById('error');
               if(data['status'] == 200){
                   error.innerHTML = "<div class='alert alert-success' role='alert'>"+data['msg']+"，请关闭本页面</div>";
                   //window.location = '/';
               }else {

                   error.innerHTML = "<div class='alert alert-success' role='alert'>"+data['msg']+"</div>";
               }
            }
        });
    });
});