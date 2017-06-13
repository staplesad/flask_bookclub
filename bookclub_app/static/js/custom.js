$('textarea').keyup(updateCount);
$('textarea').keydown(updateCount);

function updateCount(limit){
  var count = $(this).val().length;
  var output = count 
  $('#characters').text(output);
}

$(function(){
    $('a#logout').click(function(){
        if(confirm('Are you sure you want to sign out?')) {
            return true;
        }

        return false;
    });
});

