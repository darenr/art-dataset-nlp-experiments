$(function() {
	$('#submit').on('click', function(e) {
		console.log('clicked!')
		e.preventDefault();				

		$.ajax({
			url: '/',
			type: 'post',			
			data: $('form').serialize(),
			success: function() {
				console.log('Success!')
				console.log( $('form').serialize());
			},
			error: function(xhr, textStatus, errorThrown) {
				console.log(xhr.responseText);
				console.log($('form').serialize());
			}
		});
	});
});