$('.carousel').carousel({
    interval: 5000,
    pause: "false"
  });

  var $item = $('.carousel-item');
  var $wHeight = $(window).height();
  
  $item.height($wHeight);
  $item.addClass('full-screen');
  
  $('.carousel img').each(function() {
    console.log("hi");
    var $src = $(this).attr('src');
    var $color = $(this).attr('data-color');
    $(this).parent().css({
      'background-image' : 'url(' + $src + ')',
      'background-color' : $color
    });
    $(this).remove();
  });
  
  $(window).on('resize', function (){
    $wHeight = $(window).height();
    $item.height($wHeight);
  });

  $item.eq(0).addClass('active');
console.log('hiii')

$(document).ready(function() { 
  $(".test").hover(function() { 
      $(this).css("background-color", "green"); 
  }, function() { 
      $(this).css("background-color", "yellow"); 
  }); 
}); 
