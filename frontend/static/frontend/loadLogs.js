$("button").click(function() {
	let dFrom = $("input[name^='fromDate']");
	let dTo = $("input[name^='toDate']");
	let token = $("input[name^='csrfmiddlewaretoken']");

	$.post("api/loadlogs", {fromDate: dFrom.val(), toDate: dTo.val(), csrfmiddlewaretoken: token.val()}, function(data, status) {
		let tbody = $("tbody");
		tbody.empty();
	
		if(data == "" || data == "[]") //if there is no data, display an error message
		{
			tbody.val('<h3 style="color: whitesmoke; margin: 10px;">No Logs Available</h3>');
		}
		else
		{
			data = JSON.parse(data); //parse the json string into a javascript object

			//adjust json object formatting
			for (i in data)
			{
				data[i] = data[i]["fields"]
			}

			for (i in data)
			{
				//load table row template
				temp = document.getElementsByTagName("template")[0].content.querySelector("tr");
				temp = document.importNode(temp, true);

				var timestamp = new Date(data[i].startedAt) //load the startedAt value into a new Date object for localisation
				//load values into table row
				temp.getElementsByTagName("td")[0].innerText = data[i].title;
				temp.getElementsByTagName("td")[1].innerText = data[i].channel;
				temp.getElementsByTagName("td")[2].innerText = timestamp.toLocaleString();
				temp.getElementsByTagName("td")[3].innerText = data[i].game;

				tbody.append(temp); //add the row into the table
			}
		}
	})
});

$.get("api/loadlogs", function(data) {
	let tbody = $("tbody");
	let spinner = $(".spinner-border");
	spinner.remove(); //remove the spinner object (may be removed entirely at some point)
	
	if(data == "" || data == "[]") //if there is no data, display an error message
	{
		tbody.val('<h3 style="color: whitesmoke; margin: 10px;">No Logs Available</h3>');
	}
	else
	{
		data = JSON.parse(data); //parse the json string into a javascript object

		//adjust the json object formatting
		for (i in data)
		{
			data[i] = data[i]["fields"]
		}

		for (i in data)
		{
			//load table row template
			temp = document.getElementsByTagName("template")[0].content.querySelector("tr");
			temp = document.importNode(temp, true);

			var timestamp = new Date(data[i].startedAt) //load the startedAt value into a new Date object
			//insert values into row columns
			temp.getElementsByTagName("td")[0].innerText = data[i].title;
			temp.getElementsByTagName("td")[1].innerText = data[i].channel;
			temp.getElementsByTagName("td")[2].innerText = timestamp.toLocaleString();
			temp.getElementsByTagName("td")[3].innerText = data[i].game;

			tbody.append(temp); //add the row to the table 
		}
	}
});