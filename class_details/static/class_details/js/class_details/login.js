$(document).ready(function(){
    $('#login_button').click(function(event){
        event.preventDefault();
        var username = $('#id_username').val();
        var password = $('#id_password').val();
        if(!username || ! password)
            M.toast({html:'Please enter both username and password.'});
        else{
            $.ajax({
                url: '/class_details/login/',
                method: 'POST',
                data: {csrfmiddlewaretoken:$('[name="csrfmiddlewaretoken"]').val(),username:username,password:password},
                success: function(data){
                    M.toast({html:'Logged in successfully!'});
                    window.location = '/class_details/'
                },
                error: function(error){
                    console.log(error)
                    M.toast({html:error.responseText})
                }
            });
        }
    });
});