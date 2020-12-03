'use strict'


var dropIs = 0;


$(document).on('click', '#navbar_button', function(event){
	$('#navbar_collapse').css('transform', 'translateY(0)')
})

$(document).scroll(function(){
	$('#navbar_collapse').css('transform', 'translateY(-100%)')
})

var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
  var currentScrollPos = window.pageYOffset;
  if (prevScrollpos > currentScrollPos) {
    document.getElementById("navbar").style.top = "0";

  } else {
    document.getElementById("navbar").style.top = "-200px";
		if (dropIs == 1){
		document.getElementById("navbar_collapse").classList.toggle('menu_drop')
		dropIs = 0
	}
  }
  prevScrollpos = currentScrollPos;
}

function markdown_popup(){
	var target = document.getElementById('popup')
	target.classList.toggle('show')
}

function markdown_close(){
	var target = document.getElementById('popup')
	target.classList.remove('show')
}

function answer_collapse(id){
	$("#answer_collapse_" + id).toggle("fast");
}

$(document).on('click', '.answer_button', function(event){
	event.preventDefault();
	$('.answer_form_wrapper').slideToggle()
})

$(document).on('click', '.reply_button', function(event){
	event.preventDefault();
	var answer_id = $(this).attr('name')
	$('#reply_form_wrapper_' + answer_id).slideToggle()
})


$(document).on('input', '#question_form_id [name=content]', function(event){
	event.preventDefault();
	var content = $("#question_form_id [name=content]").val()
	document.getElementById('markdowned_content').innerHTML = marked(content)
})

$(document).on('input', '#answer_form_id [name=answer_content]', function(event){
	event.preventDefault();
	var content = $("#answer_form_id [name=answer_content]").val()
	document.getElementById('markdowned_content').innerHTML = marked(content)
})


$(document).on('input', '.answer_form [name=reply_content]', function(event){
	event.preventDefault();
	var id = $(this).parent().attr('id');
	var content = $(this).val()
	document.getElementById('markdowned_' + id).innerHTML = marked(content)
})

$(document).on('input', '.note_comment_form [name=content]', function(event){
	event.preventDefault();
	var content = $(this).val()
	document.getElementById('markdowned_content').innerHTML = marked(content)
})


$(document).on('click', '.question_check_button', function(event){
	$("#markdowned_content").toggle("fast");
})

$(document).on('click', '.question_check_button', function(event){
	var id = $(this).attr('id')
	$("#markdowned_reply_" + id).toggle("fast");
})

$(document).on('click', '.note_reply_check_button', function(event){
	var comment_id = $(this).parent().attr('id')
	$("#markdowned_reply_content_" + comment_id).toggle("fast");
})

$(document).on('input', '.note_reply_input', function(event){
	event.preventDefault();
	var reply_id = $(this).attr('id')
	var reply_content = $(this).val()
	document.getElementById('markdowned_' + reply_id).innerHTML = marked(reply_content)
})

/*addition*/


$(document).on('click', '.addition_open_button', function(event){
	event.preventDefault();
	$('.addition').slideToggle('fast')
})

$(document).on('input', '#addition_content_textarea', function(event){
	event.preventDefault();
	var content = $("#addition_content_textarea").val()
	document.getElementById('markdowned_addition_content').innerHTML = marked(content)
})

$(document).on('click', '#addition_content_preview', function(event){
	$("#markdowned_addition_content").toggle("fast");
})




/*poll open*/
$(document).on('click', '.poll_open_button', function(event){
	$('.poll_collapse').toggle("fast");
})

function poll_bar_toggle(){
	$(document).ready(function(){
		$(document).on('click', '.poll_option_button', function(event){
		$('.poll_bar').show("slow");
	})})
}

/* termsconditions */
$(function(){
	$(document).on('click', '[name="terms_check"]', function(event){
			if($('[name="terms_check"]').prop('checked')){
				$('.register_collapse').slideDown('fast')

			}
			else{
				$('.register_collapse').slideUp('fast')
			}
	})
})


/* note_comment_open_button */

$(document).on('click', '#login_note_comment', function(event){
	$('.comment_add_container').slideToggle('slow')
})


/* note_reply_open_button */

$(document).on('click', '.note_reply_open_button', function(event){
	var target_container = $(this).attr('name')
	$('#' + target_container).slideToggle('fast')
})
