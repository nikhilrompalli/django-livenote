$(document).ready(function(){


    $.ajax({
            url: "http://127.0.0.1:8000/LiveNote/allUserDetails/",
            success: function (data) {
                        for(i=0;i<data.length;i++){
                            userId=data[i]["id"]
                            username=data[i]["username"];
                            var user=$('<option id='+userId+' value='+username+'>'+username+'</option>');
                            $(".database_users").append(user);
                        }

                    }
     });


    $(document).on('click','.single_note_in_all_Notelist',function() {
        $('.single_note_in_all_Notelist').removeClass("change_color_on_click");
        $(this).toggleClass("change_color_on_click");

    });





});






