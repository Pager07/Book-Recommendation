$(document).ready(function () {
    console.log('READY!')
    var current_userID;
    $('#submit_user_id').on('submit' ,function(event){
        $('#recommended_books').empty()
        $.ajax({
            data:{
                userID: $('#user_id_input').val()
            },
            type: 'POST',
            url: '/swap_user'
        }).done(function(data){
            if(data.error) {
                $('#fail_alert').text(data.error).show();
                $('#success_alert').hide();
                console.log('Reached here!');
            }else{
                current_userID = $('#user_id_input').val()
                $('#home').hide();
                $('#fail_alert').hide();
                $('div#recommended_books').append(data.datax).show();
                $('#book_shelf').show()

            //    update page typ
                $('#page_type').text('Recommended books for user:' + current_userID )
                $('#page_type_info').text('The books on the left are the books I think you will like.')
            //    Update menu
                $('#main_list').show()
                $('#l_2_1').show()
            }

        });
		event.preventDefault()
    });

    $('#l_2_1').on('click', function (event) {
        $('#history_books').empty()
        $.ajax({
            data : {userID: current_userID},
            type: 'POST',
            url: '/history'
        }).done(function (data) {
            $('#recommended_books').hide()
            $('#browse_books').hide()
            $('#page_type').text('Books rated by user:' + current_userID )
            $('#page_type_info').text('The books on the left are the books that you have read.')
            if(data.error){
                $('#history_books').append('<h1>You have not rated any books</h1>').show()
            }
            else{
                $('#history_books').append(data.datax).show()
                $('#l_2_1').hide()
                $('#l_2_2').show()
            }
        })
        event.preventDefault()
    })

    $('#l_2_2').on('click', function (event) {
        $.ajax({
            data:{
                userID: current_userID
            },
            type: 'POST',
            url: '/swap_user'
        }).done(function(data){
            current_userID = $('#user_id_input').val()
            $('#home').hide();
            $('#fail_alert').hide();
            $('div#recommended_books').empty().append(data.datax).show()
            //    update page typ
            $('#page_type').text('Recommended books for user:' + current_userID )
            $('#page_type_info').text('The books on the left are the books I think you will like.')
            $('#history_books').hide()
            $('#browse_books').hide()
            $('#l_2_1').show()
            $('#l_2_2').hide()

        });
    });



    $('#l_1').on('click' , function (event) {
        $.ajax({
            data:{userID:current_userID},
            type: 'POST',
            url: '/browse'
        }).done(function (data) {
            $('#recommended_books').hide()
            $('#history_books').hide()
            $('#browse_books').empty().append(data.datax).show()
            $('#page_type').text('Explore and rate books:' + current_userID )
            $('#page_type_info').text('Click Browse agian to load new books')
            $('#l_2_1').show()
            $('#l_2_2').show()
        })
    })

    $('#l_3').on('click' , function () {
        $('#home').show()
        $('#recommended_books').empty()
        $('#history_books').empty()
        $('#browse_books').empty()
        $('#book_shelf').hide()
        current_userID = -1
    })

    // Rating selector
    $('#myRange').on('input',function () {
        $('#rating_value').html($('#myRange').val());
    })
    
    $("a.rating_new").on('click',function (event) {
        console.log('helloworld!')
        var id = event.target.id;
        console.log('id = ' + id);
    })
    // $('#submit_rating').on('click', function () {
    //     var rating_value = $('#myRange').val()
    //     $.ajax({
    //         data:{userID: current_userID ,
    //               ISBN:
    //              rating_value: rating_value},
    //               type: 'POST'
    //
    //     })
    // })







});

