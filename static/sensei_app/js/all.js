'use strict'


var dropIs = 0;


function drop (){
	if (dropIs == 0) {
		document.getElementById('navbar_collapse').classList.toggle('menu_drop')
		dropIs = 1;
	} else{
		dropIs = 0;
	}
}



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


$(document).on('click', '.question_check_button', function(event){
	$("#markdowned_content").toggle("fast");
})

$(document).on('click', '.question_check_button', function(event){
	var id = $(this).attr('id')
	console.log(id)
	$("#markdowned_reply_" + id).toggle("fast");
})
