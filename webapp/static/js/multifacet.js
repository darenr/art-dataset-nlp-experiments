$(document).ready(function() {
   $('#multi-submit').click(function(e) { 
   	console.log("clicked!")

   	var form = document.myform;

	var dataString = $(form).serialize();   	
   	var search_input = $(".search-bar #q").val()   	

   	// console.log(search_input)

	// e.preventDefault();     

	$.ajax({
	    type:'POST',
	    url:'/?q=' + search_input,	    
	    data: dataString,
	    success: function(){
	        // $('#myResponse').html(data);
	        console.log("Success! Data String: " + search_input + dataString)
	    }
	});	

	// return false;
  });
});