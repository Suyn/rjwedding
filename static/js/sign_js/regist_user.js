//获取cookie
function get_cookie(name) {
    var xsrf_cookies = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return xsrf_cookies[1];
}

//提交登录请求
$(document).ready(function(){
    $('#regist_submit').click(function (event) {
        event.preventDefault();
        user_email = $('#email').val();
        $.ajax({
            'url': '/regist',
            'type': 'post',
            'data': {
               'yourname': $('#name').val(),
               'email': user_email,
               'password1':  $('#password').val(),
               'password2':  $('#re-password').val(),
            },
            'headers':{
                 "X-XSRFTOKEN":get_cookie("_xsrf")
            },
            'success': function (data) {
                var error = document.getElementById('error');
               if(data['status'] == 200){
                   error.innerHTML = '<div class="alert alert-success" role="alert">'+data['msg']+'</div>';
                   setTimeout(function(){window.location = '/email_code?email_num='+user_email;},1000);
               }else {
                   error.innerHTML = '<div class="alert alert-success" role="alert">'+data['msg']+'</div>';
               }
            }
        });
    });
});