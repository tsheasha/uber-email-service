$(function() {
    $('#button-blue').click(function(e) {
        $('.alert-error').css("visibility", "hidden");
        $('.alert-success').css("visibility", "hidden");
        e.preventDefault();
        $.ajax({
            url: '/email/',
            data: $('#form1').serialize(),
            type: 'POST',
            dataType: "JSON",
            success: function(response) {
                if(response["error"]) {
                    $('.alert-error').html(
                        "<strong>Oh Snap!</strong> " +
                        response["error"]
                    );
                    $('.alert-error').css("visibility", "visible");
                } else {
                    $('.alert-success').html(
                        "<strong>Success!</strong> " +
                        "Your E-mail has been sent"
                    );
                    $('.alert-success').css("visibility", "visible");
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
