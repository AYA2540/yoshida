$(function () {

    // 入店・退店モーダル
    $('.my_name').on("click", function () {
        id = $(this).data("id");
        $('#enter_modal' + id).fadeIn();
        $('#out_modal' + id).fadeIn();
    });

    $('.enter_no').on("click", function () {
        id = $(this).data("id");
        $('#enter_modal' + id).fadeOut();
    });

    $('.out_no').on("click", function () {
        id = $(this).data("id");
        $('#out_modal' + id).fadeOut();
    });

    // 退会モーダル
    $('.edit').on("click", function () {
        if ($('.edit').hasClass('edit_btn')) {
            $(this).removeClass('edit_btn').addClass('back').text('戻る');
            $('.del_btn').fadeIn();
        } else {
            $(this).removeClass('back').addClass('edit_btn').text('編集');
            $('.del_btn').fadeOut();
        }
    });

    $('.delete_btn').on("click", function () {
        id = $(this).data("id");
        $('#del_modal' + id).fadeIn();
    });

    $('.del_no').on("click", function () {
        id = $(this).data("id");
        $('#del_modal' + id).fadeOut();
        $('.del_btn').fadeOut();
        $('.edit').removeClass('back').addClass('edit_btn').text('編集');
    });

    // 新規登録モーダル
    $('#regist_btn').on("click", function () {
        $('#regist_modal').fadeIn();
    });

    $('.close-modal').on("click", function () {
        $('#regist_modal').fadeOut();
    });

});