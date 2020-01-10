	function won(wid,did) {
	tselector = "#"+did+">div>" + "#"+wid
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
	/* set focus to end of search field */
	document.getElementById("q").focus();
	oldval = document.getElementById('q').value
	document.getElementById('q').value = ""
	document.getElementById('q').value = oldval
	
	/* highlight currently searched words */
	var searchArr = document.getElementById('q').value.split(" ");
	console.log('Search words: ' + searchArr)
	var divs = document.getElementsByClassName('sentence');
	for (var i = 0, length = divs.length; i < length; i++) {
		domElements = document.getElementById(divs[i].id).getElementsByTagName("div")
		console.log('Working on ' + divs[i].id)
		var found;
		/* repeat for each of two sides */
		for (var iside in [0,1]) {
			/* https://stackoverflow.com/questions/31134087/javascript-get-element-index-position-in-dom-array-by-class-or-id */
			var spanTags = domElements[iside].getElementsByTagName("span");
			/* console.log('Found ' + spanTags.length + ' in ' + divs[i].id + ' (' + iside + ')') */
			if (spanTags.length == 0) {
				/* console.log('Lets parse this: ' + domElements[iside].textContent.trim()) */
				/* console.log('Or this: ' + domElements[iside].textContent) */
				var checkArr = domElements[iside].textContent.trim().split(" ")
				var searcgReg = new RegExp( searchArr.join( "|" ), "i");
				checkArr.forEach(function(entry) {
					goodentry = entry.replace(/[,.?]/gi, '')
					/* console.log('Checking ' + goodentry) */
					var isAvailable = searcgReg.test( goodentry );
					if (isAvailable) {
						newentry = '<span class="word-hl">' + goodentry + '</span>'
						domElements[iside].innerHTML = domElements[iside].innerHTML.replace(goodentry, newentry)
					}
				});
			} else {
				for (var ispan = 0; ispan < spanTags.length; ispan++) {
					var checkArr = spanTags[ispan].textContent.split(" ")
					var searcgReg = new RegExp( searchArr.join( "|" ), "i");
					checkArr.forEach(function(entry) {
						goodentry = entry.replace(/[,.?]/gi, '')
						/* console.log('Entry: ' + goodentry) */
						var isAvailable = searcgReg.test( goodentry );
						if (isAvailable) {
							console.log(goodentry + ' regexed')
							found = spanTags[ispan];
							try {
								domElements[0].querySelector('#' + found.id).classList.add("word-hl")
							} catch(e) {
								console.log('Cannot set class for left side! (' + goodentry + ', ' + found.id + ')')
							}
							try {						
								domElements[1].querySelector('#' + found.id).classList.add("word-hl")
							} catch(e) {
								console.log('Cannot set class for right side!')
							}
						}
					});
				}
			}
		}
		/* console.log('Success.'); */
	}
  }
