// $(function() {
// 	$('#submit').on('click', function(e) {
// 		console.log('clicked!')
// 		e.preventDefault();				

// 		$.ajax({
// 			url: '/',
// 			type: 'post',			
// 			data: $('form').serialize(),
// 			success: function() {
// 				console.log('Success!')
// 				console.log( $('form').serialize());
// 			},
// 			error: function(xhr, textStatus, errorThrown) {
// 				console.log(xhr.responseText);
// 				console.log($('form').serialize());
// 			}
// 		});
// 	});
// });

$(function() {
  $("#q").focus();
  $("#q").select();

  $('#columns').masonry({
    columnWidth: 235,
    gutter: 20,
    itemSelector: '.pin'
  });

  $('#columns').imagesLoaded(function() {
    $('#columns').masonry('layout');
  });

  $(".pin img").on('click', function() {

      var el = $(this).parent();

      $(el).find(".details").slideToggle('fast', function() {
        if($(this).is(':hidden')) {
          el.removeClass("resize")
        } else {
          if($('#columns').width() > 500) {
            el.addClass("resize");
          }

          $('html, body').animate({
            scrollTop: el.offset().top - 20
          }, 'slow');
        }
        $('.pin').not(el).removeClass("resize").find('.details').hide("fast");
        $('#columns').masonry('layout');
      });

  });


});