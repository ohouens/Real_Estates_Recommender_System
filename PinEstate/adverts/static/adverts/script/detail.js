$(function(){
  $('#save').click(function(){
    alert('save in an array');
  });

  $("#pin a").click(function(e){
    // e.preventDefault();
    alert('add click to database');
  });

  $(".item").click(function(e){
    alert("save "+$(this).attr("estate")+" from "+$("#pin").attr("estate"))
  });
});
