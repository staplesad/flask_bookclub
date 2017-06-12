$('textarea').keyup(updateCount);
$('textarea').keydown(updateCount);

function updateCount(limit){
  var count = $(this).val().length;
  var output = count 
  $('#characters').text(output);
}

