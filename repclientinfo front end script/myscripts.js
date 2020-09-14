
  $(document).ready(function(){
      $("td:nth-child(4)").each(function(index){
	  			if ($(this).text() == 1) {
					$(this).parent().css('background-color','lightgreen');
				}
	  });
  });


function changeClickAction(){
	document.getElementById("exampleCheck1").onclick = reverseFiltertoAllClients;
}

function filtertoActiveClients(){
	document.getElementById("exampleCheck2").checked = false;
		var table = document.getElementById("clientTable");
	 	var tr = table.getElementsByTagName("tr");
	
		for (i = 0; i< tr.length; i++){
			tableData = tr[i].getElementsByTagName("td")[2];
			if (tableData){
				if (tableData.innerHTML== '0'){
					tr[i].style.display = "none";
				}
				else{
					tr[i].style.display = "";
				}
			}
		}
		document.getElementById("exampleCheck1").onclick = reverseFiltertoAllClients;
		
}



function reverseFiltertoAllClients(){
	var table = document.getElementById("clientTable");
	 	var tr = table.getElementsByTagName("tr");
	
		for (i = 0; i< tr.length; i++){
			tr[i].style.display = "";
		}
		document.getElementById("exampleCheck1").onclick = filtertoActiveClients;
		document.getElementById("exampleCheck2").onclick = filtertoUnassignedMailboxes;
		document.getElementById("exampleCheck2").checked = false;
		document.getElementById("exampleCheck1").checked = false;

}

function filtertoUnassignedMailboxes() {
		reverseFiltertoAllClients();
	document.getElementById("exampleCheck2").checked = true;
		document.getElementById("exampleCheck1").checked = false;
		var table = document.getElementById("clientTable");
	 	var tr = table.getElementsByTagName("tr");
	
		for (i = 0; i< tr.length; i++){
			tableData = tr[i].getElementsByTagName("td")[1];
			if (tableData){
				if (tableData.innerHTML== 'Unassigned'){
					tr[i].style.display = "";
				}
				else{
						tr[i].style.display = "none";
				}
			}
		}
	document.getElementById("exampleCheck2").onclick = reverseFiltertoAllClients;
}

		