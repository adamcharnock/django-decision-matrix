$(function () {
    var save = function ($form) {
        var url = $form.attr('action');
        var $status = $form.find('.status').empty().show();
        $.ajax(
            url,
            {
                method: 'post',
                data: $form.serialize(),
                success: function () {
                    $('<i class="fa fa-check ok" aria-hidden="true"></i>').appendTo($status).delay(1000).fadeOut();
                },
                error: function () {
                    $('<i class="fa fa-exclamation-circle error" aria-hidden="true"></i>').appendTo($status);
                }
            }
        );
    };

    $('#scoring-list input').on('change', function(event){
        save($(event.target).closest('form'));
    });

    $('#scoring-list form').on('submit', function(event){
        save($(event.target));
        event.preventDefault();
    });
});
