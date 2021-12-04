$.get("api/subbedevents", function(data) {
	tbody = document.getElementsByTagName("tbody")[0];
	spinner = document.getElementsByClassName("spinner-border")[0];
	spinner.parentElement.removeChild(spinner);
	
	if(data == "" || data == "[]") //if there is no data, display an error message
	{
		tbody.innerHTML = '<h3 style="color: whitesmoke; margin: 10px;">No Channels subscribed</h3>';
	}
	else
	{
		data = JSON.parse(data); //parse json string into javascript objects
		for (i in data) //for each log entry in the json object
		{
			//load the row template
			temp = document.getElementsByTagName("template")[0].content.querySelector("tr");
			temp = document.importNode(temp, true);
			//insert the json data into the rows
			temp.getElementsByTagName("td")[0].innerText = data[i].channel;
			temp.getElementsByTagName("td")[1].innerText = data[i].type;
			temp.getElementsByTagName("td")[2].innerText = data[i].status;
			temp.getElementsByTagName("input")[1].setAttribute("value", data[i].channel);

			tbody.appendChild(temp); //add the row element to the DOM
		}
	}
});