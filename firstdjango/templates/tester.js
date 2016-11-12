function search_sidebar()
{
	var request = new XMLHttpRequest(search_val);
	request.open('GET','/ajax_search/',true);
	request.setRequestHeader('Content-Type','application/x-www-form-urlencoded; charset=UTF-8');
	var data{'search_text': search_val};
	request.send(data);
	
	
}


<script>
	$(document).ready(function(){
		$('#search').keyup(function(){
			var search_val = $("#search").val();
			$.ajax({
				type: 'GET',
				url: "/ajax_search/",
				data:{
					'search_text' : search_val,
				},
				success: function(results){
					$("#search_results").empty();
					$("#search_results").append(results);
				}
			});
		});
	});
</script>