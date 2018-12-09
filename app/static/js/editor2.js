function clearselection()
{
	console.log('stub#112')
}
	
function pasteSelected1(tagindex)
{
	toreplace = getSelectionHtml();
	txt = window.getSelection().toString();
	txt = window.getSelection();
	/* https://stackoverflow.com/questions/972808/get-selected-node-id */
	whereareweid = txt.anchorNode.parentElement.id
	console.log('selected in ' + whereareweid)
	/* TODO: check if selection is empty */
	/* TODO: trim selection whitespaces */
	/* TODO: word-to-word view */
	toreplacecleared = toreplace.replace( /#[0-9]*/g, "" )
	replaceby = "#" + tagindex + toreplacecleared + "#"
	console.log('Text to replace: ' + toreplace + ", replace by: " + replaceby)
	if (whereareweid == 'htmlL1') {
		console.log('cond1')
		newtext = window.textL1.replace(toreplace, replaceby);
		window.textL1 = newtext
	} else if (whereareweid == 'htmlL2') {
		console.log('cond2')
		newtext = window.textL2.replace(toreplace, replaceby);
		window.textL2 = newtext
	}
	document.getElementById(whereareweid).innerHTML = newtext
}

function getSelectionHtml() {
    var html = "";
    if (typeof window.getSelection != "undefined") {
        var sel = window.getSelection();
        if (sel.rangeCount) {
            var container = document.createElement("div");
            for (var i = 0, len = sel.rangeCount; i < len; ++i) {
                container.appendChild(sel.getRangeAt(i).cloneContents());
            }
            html = container.innerHTML;
        }
    } else if (typeof document.selection != "undefined") {
        if (document.selection.type == "Text") {
            html = document.selection.createRange().htmlText;
        }
    }
    return html;
}

