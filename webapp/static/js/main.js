
$(function() {

  /*
   * replace any broken images with a better image
   */
  $(".pin img").error(function () {
    $(this).unbind("error").attr("src", "static/images/missing.png");
  });


  $("#q").attr("tabindex", 1);

  $('#columns').addClass('blur-me');


  $('#columns').masonry({
    columnWidth: 225,
    gutter: 20,
    itemSelector: '.pin',
    isAnimated: true
  });

  $('#columns').imagesLoaded(function() {
    $('.blur').removeClass();
    $('#columns').masonry('layout');
  });



  $("input:checkbox").on('click', function() {
    console.log("yeah")
    $(".search-form").submit();
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