'use strict'

//snippet

/* collapse_head open */

$(document).on("click", ".collapse_head", function(event){
	$(this).children('.collapse_head_plus').slideToggle('fast')
	$(this).next('.collapse_container').slideToggle('fast')
})


var exp_side_menu_is_open = 0
$(document).on('click', '.side_menu_button', function(event){		
	if(exp_side_menu_is_open == 0){
		$(this).children().removeClass('fa-chevron-right')
		$(this).children().addClass('fa-chevron-left')
		$('.exp_detail_fixed_menu').animate({right:'0.5rem'},300)
		exp_side_menu_is_open	= 1
	} else{
		$(this).children().addClass('fa-chevron-right')
		$(this).children().removeClass('fa-chevron-left')
		$('.exp_detail_fixed_menu').animate({right:'-80%'},300)

		exp_side_menu_is_open	= 0
	}
})


/* fixed buttons fade in/out */
var lastScrollTop = 0;
$(window).scroll(function(event){
	var st = $(this).scrollTop();
	if(exp_side_menu_is_open == 0){
		if (st < lastScrollTop){
			$(".back_top_button").stop().fadeIn("fast")
			$(".side_menu_button").stop().fadeIn("fast")
		} else {
			$(".back_top_button").stop().fadeOut("fast")
			$(".side_menu_button").stop().fadeOut("fast")
		}
	}
	lastScrollTop = st;
});


$(document).on('click', '#navbar_button', function (event) {
	$('#navbar_collapse').css('transform', 'translateY(0)')
})

$(document).scroll(function () {
	$('#navbar_collapse').css('transform', 'translateY(-100%)')
})

var prevScrollpos = window.pageYOffset;
var dropIs = 0;
window.onscroll = function () {
	var currentScrollPos = window.pageYOffset;
	if (prevScrollpos > currentScrollPos) {
		document.getElementById("navbar").style.top = "0";
	} else {
		document.getElementById("navbar").style.top = "-200px";		
		if (dropIs == 1) {
			document.getElementById("navbar_collapse").classList.toggle('menu_drop')
			dropIs = 0
		}
	}
	prevScrollpos = currentScrollPos;
}

function markdown_popup() {
	var target = document.getElementById('popup')
	target.classList.toggle('show')
}

function markdown_close() {
	var target = document.getElementById('popup')
	target.classList.remove('show')
}

function answer_collapse(id) {
	$("#answer_collapse_" + id).toggle("fast");
}

$(document).on('click', '.comment_button', function (event) {
	event.preventDefault();
	$('.comment_form_wrapper').slideToggle()
})

$(document).on('click', '.reply_button', function (event) {
	event.preventDefault();
	var answer_id = $(this).attr('name')
	$('#reply_form_wrapper_' + answer_id).slideToggle()
})


$(document).on('click', '.reply_open_button', function (event) {
	var answer_id = $(this).attr('name')
	$('#replies_container_' + answer_id).slideToggle('medium')
	var text = $(this).text();
	if (text == "返信を非表示にする")	{
		$(this).text("返信を表示する");
	}else{
		$(this).text("返信を非表示にする");
	}
})

$(document).on('input', '#question_form_id [name=content]', function (event) {
	event.preventDefault();
	var content = $("#question_form_id [name=content]").val()
	document.getElementById('markdowned_content').innerHTML = marked(content)
})

$(document).on('input', '#comment_form_id [name=comment_content]', function (event) {
	event.preventDefault();
	var content = $("#comment_form_id [name=comment_content]").val()
	document.getElementById('markdowned_content').innerHTML = marked(content)
})


$(document).on('input', '.comment_form [name=reply_content]', function (event) {
	event.preventDefault();
	var id = $(this).parent().attr('id');
	var content = $(this).val()
	document.getElementById('markdowned_' + id).innerHTML = marked(content)
})

$(document).on('input', '.note_comment_form [name=content]', function (event) {
	event.preventDefault();
	var content = $(this).val()
	document.getElementById('markdowned_content').innerHTML = marked(content)
})


$(document).on('click', '.question_check_button', function (event) {
	$("#markdowned_content").toggle("fast");
})

$(document).on('click', '.question_check_button', function (event) {
	var id = $(this).attr('id')
	$("#markdowned_reply_" + id).toggle("fast");
})

$(document).on('click', '.note_reply_check_button', function (event) {
	var comment_id = $(this).parent().attr('id')
	$("#markdowned_reply_content_" + comment_id).toggle("fast");
})

$(document).on('input', '.note_reply_input', function (event) {
	event.preventDefault();
	var reply_id = $(this).attr('id')
	var reply_content = $(this).val()
	document.getElementById('markdowned_' + reply_id).innerHTML = marked(reply_content)
})

/*addition*/


$(document).on('click', '.addition_open_button', function (event) {
	event.preventDefault();
	$('.addition_form').slideToggle('fast')
})

$(document).on('input', '#addition_content_textarea', function (event) {
	event.preventDefault();
	var content = $("#addition_content_textarea").val()
	document.getElementById('markdowned_addition_content').innerHTML = marked(content)
})

$(document).on('click', '#addition_content_preview', function (event) {
	$("#markdowned_addition_content").toggle("fast");
})




/*poll open*/
$(document).on('click', '.poll_open_button', function (event) {
	$('.poll_collapse').toggle("fast");
})

/* termsconditions */
$(function () {
	$(document).on('click', '[name="terms_check"]', function (event) {
		if ($('[name="terms_check"]').prop('checked')) {
			$('.register_collapse').slideDown('fast')

		} else {
			$('.register_collapse').slideUp('fast')
		}
	})
})


/* note_comment_open_button */

$(document).on('click', '#login_note_comment', function (event) {
	$('.comment_add_container').slideToggle('slow')
})


/* note_reply_open_button */

$(document).on('click', '.note_reply_open_button', function (event) {
	var target_container = $(this).attr('name')
	$('#' + target_container).slideToggle('fast')
})


$(document).on('click', '.sidebar_head', function (event) {
	$(this).next().slideToggle('fast')
	$(this).classToggle('clicked')
})