$('textarea').keyup(updateCount);
$('textarea').keydown(updateCount);

function updateCount(limit){
  var count = $(this).val().length;
  var output = count 
  $('#characters').text(output);
}

$(function(){  // confirmation on sign out
    $('a#logout').click(function(){
        if(confirm('Are you sure you want to sign out?')) {
            return true;
        }

        return false;
    });
});


$(document).click(function(e) {  // lets user click outside the mobile menu to close it
    if (!$(e.target).is('a')) {
        $('.collapse').collapse('hide');        
    }
});

