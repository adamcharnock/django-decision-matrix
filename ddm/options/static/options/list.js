$(function(){
    $('th form').on('click', function(e){
        e.stopPropagation();
    }).on('change', function(e){
        $(this).submit();
    });
});
