$(function () {
    var save = function ($form) {
        var url = $form.attr('action');
        var $status = $form.find('.status').empty().show();
        var $input = $form.find('input[name=value]');
        $input.val(
            Math.min(
                Math.max($input.val(), $input.attr('min')),
                $input.attr('max')
            )
        );
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

    $('#weighting-list input').on('change', function(event){
        save($(event.target).closest('form'));
    });

    $('#weighting-list form').on('submit', function(event){
        save($(event.target));
        event.preventDefault();
    });
});
