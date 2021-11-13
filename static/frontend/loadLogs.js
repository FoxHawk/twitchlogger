$.get("api/loadlogs", function(data) {
	console.log(data);
	tbody = document.getElementsByTagName("tbody")[0];
	spinner = document.getElementsByClassName("spinner-border")[0];
	spinner.parentElement.removeChild(spinner);
	
	if(data == "" || data == "[]") //if there is no data, display an error message
	{
		tbody.innerHTML = '<h3 style="color: whitesmoke; margin: 10px;">No Logs Available</h3>';
	}
	else
	{
		data = JSON.parse(data);

		for (i in data)
		{
			data[i] = data[i]["fields"]
		}

		for (i in data)
		{
			temp = document.getElementsByTagName("template")[0].content.querySelector("tr");
			temp = document.importNode(temp, true);

			var timestamp = new Date(data[i].startedAt)
	
			temp.getElementsByTagName("td")[0].innerText = "TODO" //data[i].title;
			temp.getElementsByTagName("td")[1].innerText = data[i].channel;
			temp.getElementsByTagName("td")[2].innerText = timestamp.toLocaleString();
			temp.getElementsByTagName("td")[3].innerText = "TODO" //data[i].length;
			tbody.appendChild(temp);
		}
	}
});