$(".response_form").hide();

function format_responses() {
  //click to toggle
  var a = $(".course_questions");
  console.log("adding click handlers to"+a.length+" presentations");
  $(".course_questions").click(function(event) {
    console.log("clicked on "+this.innerHTML);
      $(this).find(".response_form").slideToggle();
  });
}

format_responses();
