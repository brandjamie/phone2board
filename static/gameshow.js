
   
function requestUpdate() {
  if (window.XMLHttpRequest)
        {
        xmlhttp = new XMLHttpRequest();
        }
        xmlhttp.open("GET",window.updatepage,true);
        xmlhttp.onreadystatechange = updateJson;
        xmlhttp.send();
        }

function updateJson() {
       var result; 
       var resultJson; 


        if (xmlhttp.readyState==4) { 
	   // window.alert("received statechange");
	  //  window.alert(xmlhttp);
	setTimeout(requestUpdate,0);
 	    result = xmlhttp.responseText; 
	 //   window.alert("result");
	    if (result != "") {
 		resultJson = JSON.parse(result);  
		window.updatefunc(resultJson);
	    }
	}

}
    
function hidediv () {
    for (var i=0; i<arguments.length; i++)
    {
	var divid = document.getElementById(arguments[i]);
	divid.style.display="none";
    }
}

   
function showdiv () {
for (var i=0; i<arguments.length; i++)
    {
	var divid = document.getElementById(arguments[i]);
	divid.style.display="block";
    }
}

function writediv (divname,htmltowrite) {
var divid = document.getElementById(divname);
divid.innerHTML = htmltowrite;
}


function maketeamlist () {
 var team = arguments[0];
  var teamhtml ="";
   for (i=0;i<team.length;i++)
    {
	       if (team[i]!=""){
	       teamhtml = teamhtml+"<li id='"+team[i]+"' class='teamitem'>"+team[i]+"</li>";
	       }
    }
    if (teamhtml=="") {teamhtml="No teams connected";}
    document.getElementById('teamlist').innerHTML=teamhtml;
}








function maketable () {
    // function to make a table from an array of arrays.
    // the first array (arguments[0] is a list of column titles

    var coltitles =  arguments[0];
    var tablewidth = arguments.length-1;
    
    // arguments.length-1  must = arguments[0].length
    if (coltitles.length != tablewidth) {
//    	window.alert("failure making table - incorrect number of collumns");
     	return false;
    }
    var tableheight = 0;
    // get tableheight
    for (i=0; i<tablewidth;i++) 
    {
     	if (arguments[i+1].length>tableheight)
     	{
     	    tableheight=arguments[i+1].length;
     	}
    }
    tableheight++;
    var tablehtml ="<table id='teamtable'>";

    for (i=0;i<tableheight;i++)
    {
    tablehtml=tablehtml+"<tr>"
	
    for (j=0;j<tablewidth;j++)
	{
     	    tablehtml=tablehtml+"<td>";
     	    if (i==0)
    	    {tablehtml=tablehtml+arguments[0][j];}
     	    else 
     	    {
     		var thishtml = arguments[j+1][i-1];
     		if (thishtml!="") 
     		{tablehtml=tablehtml+thishtml}
     	    }
     	    tablehtml=tablehtml+"</td>"
	    
    	}
    tablehtml=tablehtml+"</tr>";
    }
    tablehtml=tablehtml+"</table>";
    return tablehtml;
}













function sendmessage (message,messageurl) {
		if (window.XMLHttpRequest)
		{
		xmlhttpm = new XMLHttpRequest();
		}
		xmlhttpm.open("GET",messageurl+"?"+message,true);
		xmlhttpm.setRequestHeader("Content-type","application/x-www-form-urlencoded");
		xmlhttpm.send();
 //   requestUpdate();
}
