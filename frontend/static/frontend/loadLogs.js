function loadTable(data)
{
	let tbody = $("tbody");
	tbody.empty();

	for (i in data)
	{
		data[i] = data[i]["fields"]
	}

	for (i of data)
	{
		temp = document.getElementsByTagName("template")[0].content.querySelector("tr");
		temp = document.importNode(temp, true);

		var timestamp = new Date(i.datetimestamp)
	
		temp.getElementsByTagName("td")[0].innerText = i.title;
		temp.getElementsByTagName("td")[1].innerText = i.channel;
		temp.getElementsByTagName("td")[2].innerText = timestamp.toLocaleString();
		temp.getElementsByTagName("td")[3].innerText = i.type;
		temp.getElementsByTagName("td")[4].innerText = i.game;
		tbody.append(temp);
	}
}

$("button.btn-primary").click(function() {
	let dFrom = $("input[name^='fromDate']");
	let dTo = $("input[name^='toDate']");
	let token = $("input[name^='csrfmiddlewaretoken']");

	$.post("api/loadlogs", {fromDate: dFrom.val(), toDate: dTo.val(), csrfmiddlewaretoken: token.val()}, function(data, status) {
		if(data == "" || data == "[]") //if there is no data, display an error message
		{
			tbody.val('<h3 style="color: whitesmoke; margin: 10px;">No Logs Available</h3>');
		}
		else
		{
			data = JSON.parse(data);

			loadTable(data);
		}
	})

	//ensure all checkboxes are checked when the page is loaded
	let checkboxes = $(".checkbox-menu").find("input");
	for (i of checkboxes)
	{
		$(i).prop("checked", true);
		$(i).closest("li").prop("active", true);
	}
	//clear the search bar
	let search = $("input.form-control");
	search.val("");
});

$.get("api/loadlogs", function(data) {
	let tbody = $("tbody");
	let spinner = $(".spinner-border");
	spinner.remove();
	
	if(data == "" || data == "[]") //if there is no data, display an error message
	{
		tbody.val('<h3 style="color: whitesmoke; margin: 10px;">No Logs Available</h3>');
	}
	else
	{
		data = JSON.parse(data);

		loadTable(data);
	}
});