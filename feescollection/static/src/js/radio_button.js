$(function(){
    $("input[name='user_type']").change(function(){
        if (this.value == 'institute') {
        $("#compny_id").removeClass("d-none");
        $("#currncy_id").removeClass("d-none");

        }
        if (this.value == 'student') {
             $("#compny_id").addClass("d-none");
            $("#currncy_id").addClass("d-none");
        }
    });
});