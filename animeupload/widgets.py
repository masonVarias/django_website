from django import forms
from django.utils.safestring import mark_safe
from animeupload.models import Movie, TVShow
from django.utils.html import escape
from itertools import chain

class seriesWidget(forms.widgets.TextInput):

	def render(self,name,value,attrs=None):

		debug =""

	#	shows = Show.objects.all().order_by("english_title")
		shows = chain(Movie.objects.all().order_by("english_title"),TVShow.objects.all().order_by("english_title"))
		rowstart = ['<div class = "row" style="display: flex;">','','']
		rowend = ['', '', '</div>']

		content = ""
		counter = 0
		for show in shows:
			content = content + rowstart[counter%3]
			content =  content + '<div class = "col-sm-4 low_padding" style="outline:1px solid black;"><div class = "col-sm-6 low_padding"><img src = "'
			content = content + show.image.url
			content = content + '"class="img-rounded" align = "left" style="width:80px;height:100px"></div><div class="col-sm-6 low_padding"> <b id="'
			content = content + str(escape(show.id)) +  '"class = "show_names">' + escape(show.english_title.title()) + "</b>"
			content = content + "<br> <select id='season'> <option value="">all</option>"
			if hasattr(show,"total_seasons") and show.total_seasons > 1:
				for curr in range(show.total_seasons):
					content = content + "<option value = '" + str((curr + 1)) + "'> season " + str((curr + 1)) + "</option>"
			content = content + '</select><button = type="button" class="btn_show_selection">select</button></div></div>'
			content = content + rowend[counter%3]

			counter = counter + 1

		debug = debug + "out " + str((counter %3)) + ": "
		if counter %3 != 0:
			for curr in range(3 - (counter %3)):
				content = content + '<div class = "col-sm-4 low_padding" style="outline:1px solid black;"></div>'
				debug = debug + str((counter %3))
			content = content + "</div>"

		html = '<div class ="col-xs-4">'
		html = html + super(seriesWidget, self).render(name,value,attrs={"id" : "id_watch_order" ,"readonly":"True"})	
		html = html +"""

			  <br>
			<button type="button" class="btn btn-info btn-lg" id="btn_update">update</button>
			<button type="button" class="btn btn-info btn-lg" id="btn_clear">clear</button>
			</div>
			 <div class ="col-xs-4">
			 <h3><u>series order</u>
			 <!-- Trigger the modal with a button -->
			  <button type="button" class="btn btn-info btn-xs" data-toggle="modal" data-target="#myModal">select shows</button>
			  </h3>
			<ol id ="the_list">
			</ol>
			</div>
			
			  <br>
			  
			  <!-- Modal -->
			  <div class="modal fade" id="myModal" role="dialog">
			    <div class="modal-dialog">
			    
			      <!-- Modal content-->
			      <div class="modal-content">
			        <div class="modal-header">
			          <button type="button" class="close" data-dismiss="modal">&times;</button>
			          <h4 class="modal-title">Modal Header</h4>
			        </div>
			        <div class="modal-body">
	        	""" + content + """
	        </div>
	        <div class="modal-footer">
	          <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
	        </div>
	      </div>
	      
	    </div>
	  </div>
			"""
		scripts = """
		<script>
	$(".btn_show_selection").click(function(event){
		var nameblock = $(this).siblings(".show_names");
		var img = $(this).siblings(".show_names");
		var selected_id = nameblock.attr("id");
		var title = nameblock.text();
		var season = $(this).siblings("#season").val();
		var li_id = "#" + selected_id +":"+ season;
		
		if(season != ""){
			season = ":" + season;
		}
		$("#the_list").append("<li id=" +selected_id + season + ">" +title + season + "</li>");
		$(nameblock).clone().appendTo("#the_lsit li:last-child").append("season" +season);

		$(".close").trigger("click");
	});
	
	$("#btn_update").click(function(event){
		$("#id_watch_order").val("");
		$("#the_list li").each(function(){
			var trimed = $.trim($(this).text());
			$("#id_watch_order").val( $("#id_watch_order").val() + $(this).attr("id") + ",");
		});
		$("#id_watch_order").val($("#id_watch_order").val().slice(0,-1));
	});
	
	$("#btn_clear").click(function(){
		$("#the_list").empty();
		$("#id_watch_order").val("");
	});
	
	$(function(){
		$("#the_list").sortable();
		$("#the_list").disableSelection();
	});
</script>
		"""

#		html = ""
#		for show in shows:
#			html= html + str(show.english_title)
		return mark_safe(html + scripts)