$(document).ready(function() {
    $(".accept").click(function(){
      id = $(this).attr('value');
	  $.ajax({
	    url: "http://localhost:5000/updateReservation",
	    type: "GET",
	    dataType: "json",
	    data: {id: id, answer: "Aceito"}
	  }).done(function(data){
	  	alert(data.return);
	  });
    });

    $(".reject").click(function(){
      id = $(this).attr('value');
	  $.ajax({
	    url: "http://localhost:5000/updateReservation",
	    type: "GET",
	    dataType: "json",
	    data: {id: id, answer: "Rejeitado"}
	  }).done(function(data){
	  	alert(data.return);
	  });
    });
});
