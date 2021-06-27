$(document).ready(function(){
    $('#student_table').on('click','.student_status',function(){
        var student_id = $(this).closest('.student_details').data('id');
        var status = $(this).prop('checked')?1:0;
    
        $.ajax({
            url: '/class_details/update_status/',
            method: 'POST',
            data: {csrfmiddlewaretoken:$('[name="csrfmiddlewaretoken"]').val(),student_id:student_id,status:status},
            success: function(data){
                M.toast({html:'Status updated successfully!'});
            },
            error: function(error){
                console.log(error);
            }
        });
    });

    $('#add_class').click(function(){
        var class_name = $('#class_name').val();
        if(!class_name)
        {
            M.toast({html:'Please enter class name.'});
            return
        }
        $.ajax({
            url: '/class_details/add_class/',
            method: 'POST',
            data: {csrfmiddlewaretoken:$('[name="csrfmiddlewaretoken"]').val(),class_name:class_name},
            success: function(data){
                if(data=='Class exists already!')
                    M.toast({html:'Class exists already!'});
                else
                    M.toast({html:'Class added successfully!'});
                $('#class_name').val('');
            },
            error: function(error){
                console.log(error);
            }
        });
    });
});