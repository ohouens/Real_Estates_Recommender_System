$(function(){
  $('#save').click(function(){
    alert('save in an array');
  });

  $("#pin a").click(function(e){
    e.preventDefault();
    alert('add click to database');
  });

  $(".item").click(function(e){
    e.preventDefault();
    url = "join/"+$(this).attr("estate");
    item = $(this);
    $.get(url, function(data){
      document.location.href = "../.."+item.find('a').attr('href');
    });
  });
});
