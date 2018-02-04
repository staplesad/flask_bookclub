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


$(function() {
  $("form[id=addpollform]").each(function() {
    var $this = $(this);
    $this.find("button[data-toggle=options-add]").click(function() {
      var target = document.getElementById('poll-options');
      console.log(target);
    var inputs = target.getElementsByTagName('input');
    var numInputs = inputs.length;
    if (numInputs > 9){
      console.log("too many options!");
      return;
    }
    var new_id = "optionList-"+numInputs;
    console.log(new_id);
    var newrow = document.createElement("input");
    newrow.id = new_id;
    newrow.name = new_id;
    newrow.type="text";
    var breakrow = document.createElement("br");
    target.appendChild(newrow);
    target.appendChild(breakrow);
    target.appendChild(breakrow.cloneNode()); 
    });
    });
  });
