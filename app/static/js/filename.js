	function won(wid,did) {
	/*tselector = "div#p2 p#l2 span#w1"
	tselector = "div#"+did+" div span#" + wid*/
	tselector = "#"+did+">div>" + "#"+wid
	/*console.log("tselector: "+tselector);*/
	els = document.querySelectorAll(tselector);
	for ( var i = 0; i < els.length; i++) {
		/* #BFB63B - green, sort of */
		/* #FFFF00 - yellow original */
		/* #F26B6B - fancy red */
		els[i].style = "background-color: #FFFF00";
	}
	/*translation.style="background-color: #FFFF00";*/
	}
	function woff(wid,did) {
	/*tselector = "div#"+did+" div span#" + wid;*/
	tselector = "#"+did+">div>" + "#"+wid
	els = document.querySelectorAll(tselector);
		for ( var i = 0; i < els.length; i++) {
			els[i].style = "";
		}
	}
	window.onload = function () {
	var rumples = document.getElementsByClassName("word");
	/* console.log('we have elts: '+rumples.length); */
	for ( var i = 0; i < rumples.length; i++) {
		/* console.log('working on element '+i); */
		rumples[i].onmouseover = function() { won(this.id,this.parentNode.parentNode.id); };
		rumples[i].onmouseout = function() { woff(this.id,this.parentNode.parentNode.id); };
		rumples[i].onmousedown = function() { won(this.id,this.parentNode.parentNode.id); };
		rumples[i].onmouseup = function() { woff(this.id,this.parentNode.parentNode.id); };
	}
	document.getElementById("q").focus();
  }