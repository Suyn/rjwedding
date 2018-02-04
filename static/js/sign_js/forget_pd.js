//获取cookie
function get_cookie(name) {
    var xsrf_cookies = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return xsrf_cookies[1];
}

//提交登录请求
$(document).ready(function(){
    $('#forget_submit').click(function (event) {
        event.preventDefault();
        $.ajax({
            'url': '/forget',
            'type': 'post',
            'data': {
               'email': $('#email').val(),
            },
            'headers':{
                 "X-XSRFTOKEN": get_cookie("_xsrf"),
            },
            'success': function (data) {
                var error = document.getElementById('error');
               if(data['status'] == 200){
                   error.innerHTML = "<div class='alert alert-success' role='alert'>"+data['msg']+"</div>";
               }else {
                   error.innerHTML = "<div class='alert alert-success' role='alert'>"+data['msg']+"</div>";
               }
            }
        });
    });
});