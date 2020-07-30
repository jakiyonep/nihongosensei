'use strict'
function confirmation(){
      ret = confirm("Are you sure you want to submit?");
  }

function color_change(pk){
	document.getElementById('original-' + pk).classList.toggle('correction_visible')
}

$('.correction_btn').on('click', function(){
    var id =  $(this).attr("id");
    $('#desc-' + id).slideToggle('normal');
		$('#' + id).toggleClass('correction_button')
});


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



function openNav() {
  document.getElementById("articles_sidebar").classList.toggle('open_nav')
}

$(function(){
	$('#sentence_casual_btn').on('click', function(){
		$('.sentence_casual').slideToggle('normal');
	})
})

$(function(){
	$('#sentence_yomi_btn').on('click', function(){
		$('.sentence_yomi').slideToggle('normal');
	})
})

$(function(){
	$('#sentence_en_btn').on('click', function(){
		$('.sentence_en').slideToggle('normal');
	})
})

$(function(){
	$('#question_answer_btn').on('click', function(){
		$('.question_answer').slideToggle('normal');
	})
})

$(function(){
	$('#question_yomi_btn').on('click', function(){
		$('.question_yomi').slideToggle('normal');
	})
})

$(function(){
	$('#question_en_btn').on('click', function(){
		$('.question_en').slideToggle('normal');
	})
})


$(function(){
	$('.answer_button_a').on('click', function() {
		var target_id = $(this).attr('id');
		$('#collapse-' + target_id).slideToggle('slow');
})
});

$(function(){
	$('#filter_button').on('click', function() {
		$('.filter_collapse').slideToggle('normal	');

})
});
