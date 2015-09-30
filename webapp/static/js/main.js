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
  $("#q").attr("tabindex", 1);

  $('#columns').addClass('blur-me');


  $('#columns').masonry({
    columnWidth: 235,
    gutter: 20,
    itemSelector: '.pin',
    isAnimated: true
  });

  $('#columns').imagesLoaded(function() {
    $('#columns').masonry('layout');
    console.log("finsihed loading images");
  });

  /*
   * replace any broken images with a better image
   */
  $(".pin img").error(function () {
    $(this).unbind("error").attr("src", "static/images/missing.png");
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

$(document).ready(function(){ 

  // Maintain State of Checkboxes
  $(":checkbox").on("change", function(){
    var checkboxValues = {};
    $(":checkbox").each(function(){
      checkboxValues[this.id] = this.checked;
    });
      
    $.cookie('checkboxValues', checkboxValues, { expires: 7, path: '/' });
  });

  function repopulateCheckboxes(){    
    var checkboxValues = $.cookie('checkboxValues');    
        
    if(checkboxValues){    

      Object.keys(checkboxValues).forEach(function(element) {    
        var checked = checkboxValues[element];
        $("#" + element).prop('checked', checked);
      });
    }
  }

  $.cookie.json = true;
  repopulateCheckboxes();

});
