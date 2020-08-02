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
