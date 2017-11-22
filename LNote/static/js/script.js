$(document).ready(function(){
        $.ajax({
          url: "http://127.0.0.1:8000/LiveNote/notebooks/",
          success: function(res){
            for(i=0;i<res.length;i++){
                data=res[i]
                var NoteBookName=data["title"]
                var NoteBookTag=data["tag"]
                var id=data["id"]
                var rightNotebookContainer=$('<div id="r'+id+'" class="notebook"><div class="book_name"><div class="book_tools"><div></div><div class="w3-padding w3-large w3-text-black"><a  class="close" href="#popup1"><i class="fa fa-trash"></i></a></div></div><p class="bookname_p">'+NoteBookName+'</p></div><div class="book_desp"><p>'+NoteBookTag+'</p></div></div>');
                var leftNotebookContainer=$('<div id="l'+id+'" class="leftside_notebooks_list"><p>'+NoteBookName+'</p></div>');
                $(".myNotebooks_container").append(rightNotebookContainer);
                $(".leftside_myNotebooks_details").append(leftNotebookContainer);
            }
          }
        });
        $.ajax({
          url: "http://127.0.0.1:8000/LiveNote/sharedNotesOfUser/",
          success: function(res){
            for(i=0;i<res.length;i++){
                data=res[i]
                var sharedByName=data["sharedByName"]
                var sharedNoteId=data["note"]
                var id=data["id"]
                var sharedNoteName;

                $.ajax({                                                                //for notebook details by nb id
                  url: "http://127.0.0.1:8000/LiveNote/note/"+sharedNoteId+"/",
                  success: function(innerRes){
                    sharedNoteName=innerRes[0]['title'];
                    var newNote=$('<div id="s'+id+'" class="sharedNotes"><div class="shared_notes_name"><div class="shared_notes_tools"><div></div><div class="w3-padding w3-large w3-text-black"><a  class="close" href="#popup1"><i class="fa fa-trash"></i></a></div></div><p>'+sharedNoteName+'</p></div><div class="share_note_desp"><p>By '+sharedByName+'</p></div></div>');
                    $(".sharedNotebook_container").append(newNote);
              }
             });
            }
          }
        });

    $(".create_project_btn").click(function(){
        var newNoteBookName = $('.login-form').find('input[name="notebook_name"]').val();
		var newNoteBookTag = $('.login-form').find('input[name="tag"]').val();
		newNoteBook=new Object();
		newNoteBook["title"]=newNoteBookName;
		newNoteBook["tag"]=newNoteBookTag;
        $.ajax({url: "http://127.0.0.1:8000/LiveNote/notebooks/",
            type: 'post',
            headers:{
                "X-CSRFToken":csrftoken
            },
            data: newNoteBook,
            dataType: 'json',
            success: function (data) {
                location.reload();

            }
        });

    });

var currentNoteBookId;
    $(document).on('click','.leftside_notebooks_list,.book_desp',function() {
    	var divId1=$(this).parent().attr('id');
    	var divId2=$(this).attr('id');
    	if(divId1)
    	    Id=divId1.slice(1,divId1.length)
    	else
    	    Id=divId2.slice(1,divId2.length)
    	currentNoteBookId=Id;
    	$.ajax({
          url: "http://127.0.0.1:8000/LiveNote/notebook/"+Id+"/",
          success: function(res){
            $.ajax({                                                                //for notebook details by nb id
                  url: "http://127.0.0.1:8000/LiveNote/notebookDetails/"+Id+"/",
                  success: function(innerRes){
                    nbTitle=innerRes[0]['title'];
                    nbTime=innerRes[0]['time'];
                    $(".note_matter").text(nbTitle);
                    $("#date").text(nbTime.slice(0,10));
                    $("#time").text(nbTime.slice(11,16));
                  }
                });


            for(i=0;i<res.length;i++){
                noteId=res[i]["id"]

                $.ajax({
                  url: "http://127.0.0.1:8000/LiveNote/note/"+noteId+"/",       //geting all notes in selected notebook
                  success: function(innerRes){
                    noteId=innerRes[0]["id"];
                    noteTitle=innerRes[0]["title"];
                    noteTime=innerRes[0]["time"];
                    date=noteTime.slice(0,10)
                    noteTime=noteTime.slice(11,16)
                    var newNote=$('<div id='+noteId+' class="single_note_in_all_Notelist"><p class="date_time">'+date+'</p><p class="time">'+noteTime+'</p><br><p class="title">'+noteTitle+'</p><div class="status_div"><select class="status"><option id="1" value="incompleted">Incompleted</option><option id="0" value="completed">Completed</option></select></div>');
    	            $(".list_of_all_notes_section").append(newNote);
                  }
                });
            }
          }
        });
	});
    $(document).on('click','.add_note_btn',function() {
        var noteName=$('#note_name').val()
        newNote=new Object();
		newNote["title"]=noteName;
		newNote["notebook"]=currentNoteBookId;
		newNote["tag"]="demo";
        $.ajax({url: "http://127.0.0.1:8000/LiveNote/notebook/"+currentNoteBookId+"/",
            type: 'post',
            headers:{
                "X-CSRFToken":csrftoken
            },
            data: newNote,
            dataType: 'json',
            success: function (data) {
                    var Id=data["id"];
                    var time=data['time'];
                    var newNote=$('<div id='+Id+' class="single_note_in_all_Notelist"><p class="date_time">'+time+'</p><br><p id="added_note_name">'+noteName+'</p></div>');
    	            $(".list_of_all_notes_section").append(newNote);
            }
        });

	});

	$(document).on('click','.close',function() {
    	var divId=$(this).parent().siblings().parent().parent().parent().attr('id');
    	var rmId=divId.slice(1,divId.length)
    	 $(document).on('click','.del_notebook',function() {
                $.ajax({url: "http://127.0.0.1:8000/LiveNote/notebookDetails/"+rmId+"/",
                    type: 'delete',
                    headers:{
                        "X-CSRFToken":$.cookie("csrftoken")
                    },
                    success: function (data) {
                        $('#r'+rmId).remove();
                        $('#l'+rmId).remove();
                    }
                });
             location.reload();
        });
	});




	$(".logout_logo").click(function(){
      url = "http://127.0.0.1:8000/logout";
      $(location).attr("href", url);
   });


      $(document).on('click','.leftside_notebooks_list, .book_desp, .share_note_desp',function() {
    	$.ajax({
          url: "note",
          success: function(data){
             $(".right").html(data);
             $("#note_section").hide();
          }
        });
    });

    $(".status").change(function() {
          var id = $(this).children(":selected").attr("id");
        });

	var currentNoteId,currentNoteName;
     $(document).on('click','.single_note_in_all_Notelist',function() {
        $("#note_section").show();
    	var Id=$(this).attr('id');
    	if(Id[0]=='s'){
    	    Id=Id.slice(1,Id.length);
    	    $.ajax({
              url: "http://127.0.0.1:8000/LiveNote/sharedNoteById/"+Id+"/",
              success: function(res){
                    title=res[0]['title'];
                    time=res[0]['time'];
                    text=res[0]['text'];
                    sharedByname=res[0]['sharedByName']
                    date=time.slice(0,10);
                    time=time.slice(10,time.length);
                    $(".header_note_name h2").text(title);
                    $(".header_note_sharedBy p").text(sharedByname);
                    $(".header_note_date p").text(date);
                    $(".header_note_time p").text(time);
                    $(".note_content_matter").text(text);
              }
            });
    	}
    	else
    	{
            $(".header_note_sharedBy p").hide();
            currentNoteId=Id;
            $.ajax({
              url: "http://127.0.0.1:8000/LiveNote/note/"+Id+"/",
              success: function(res){
                    title=res[0]['title'];
                    time=res[0]['time'];
                    text=res[0]['text'];
                    date=time.slice(0,10);
                    time=time.slice(11,16);
                    currentNoteName=title;
                    $(".header_note_name h2").text(title);
                    $(".header_note_date p").text(date);
                    $(".header_note_time p").text(time);
                    $(".note_content_matter").text(text);
              }
            });
        }
	});

    $(document).on('click','#close',function() {
                $(".delpopup2 h2").text("Are You Sure to Delete "+currentNoteName+" Note");
        });


    $(document).on('click','.del_note',function() {
                $.ajax({url: "http://127.0.0.1:8000/LiveNote/note/"+currentNoteId+"/",
                    type: 'delete',
                    headers:{
                        "X-CSRFToken":csrftoken
                    },
                    success: function (data) {
                    }
                });
                $('#'+currentNoteId).remove();
        });

        $(".database_users").change(function() {
          var id = $(this).children(":selected").attr("id");
        });

        $(document).on('click','.share_note_btn',function() {
                var Id=$(".database_users").children(":selected").attr("id");
                var user=$('.database_users option:selected').text();
                shareNote=new Object();
                shareNote["title"]=$("#note_header_name").text();
                shareNote["text"]=$(".note_content_matter").text();
                shareNote["sharedWithId"]=Id;
                shareNote["note"]=currentNoteId;
                $.ajax({url: "http://127.0.0.1:8000/LiveNote/allSharedNotes/",
                    type: 'post',
                    headers:{
                        "X-CSRFToken":csrftoken
                    },
                    data: shareNote,
                    dataType: 'json',
                    success: function (data) {
                    }
                });
        });
    $(document).on('click','#save',function() {
                noteData=new Object();
                noteData["title"]=$("#note_header_name").text();
                noteData["tag"]="demo";
                noteData["text"]=$(".note_content_matter").text();
                noteData["notebook"]=currentNoteBookId;
                $.ajax({url: "http://127.0.0.1:8000/LiveNote/note/"+currentNoteId+"/",
                    type: 'put',
                    headers:{
                        "X-CSRFToken":csrftoken
                    },
                    data:noteData,
                    dataType:'json',
                    success: function (data) {
                    }
                });
        });

var currentSharedNoteId;

    $(document).on('click','.share_note_desp',function() {
    	var divId1=$(this).parent().attr('id');
    	$(".addNote").hide();
        var Id=divId1.slice(1,divId1.length)
    	currentSharedNoteId=Id;
    	var sharedHeading="Shared Notes";
    	$(".note_matter").text(sharedHeading);
    	$.ajax({
          url: "http://127.0.0.1:8000/LiveNote/sharedNotesOfUser/"+currentSharedNoteId+"/",
          success: function(res){
            for(i=0;i<res.length;i++){
                sharedNoteTitle=res[i]['title'];
                sharedNoteId=res[i]['id'];
                sharedNoteTime=res[i]['time'];
                var newNote=$('<div id="s'+sharedNoteId+'" class="single_note_in_all_Notelist"><p class="date_time">'+sharedNoteTime+'</p><br><p>'+sharedNoteTitle+'</p></div>');
    	        $(".list_of_all_notes_section").append(newNote);
            }
        }
      });
    });



    $(".status").change(function() {
          var id = $(this).children(":selected").attr("id");
        });


}); 

  
 