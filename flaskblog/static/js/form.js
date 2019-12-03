$(document).ready(function () {
    console.log('READY!')
    var current_userID;
    var current_isbn;
    var number_books_rated;
    var trending_books_tally = 0 ;
    var current_page = 'home';
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
                $('#main_list2').hide();
                $('div#recommended_books').empty().append(data.datax).show();
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
            $('#trending_books').hide()
            $('#page_type').text('Books rated by user:' + current_userID )
            $('#page_type_info').text('The books on the left are the books that you have read.')
            if(data.error){
                $('#history_books').append('<h1>You have not rated any books</h1>').show()
            }
            else{
                $('#history_books').empty().append(data.datax).show()
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


// Browse
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

    $('.log_out').on('click' , function () {
        $('#home').show()
        $('#recommended_books').empty()
        $('#history_books').empty()
        $('#browse_books').empty()
        $('#book_shelf').hide()
        $('#page_type2').hide()
        $("#success-activate-alert").hide()
        $('#new_user_id').text('Loading..')
        current_userID = -1
        trending_books_tally = 0
    })

    // Rating selector
    $('#myRange').on('input',function () {
        $('#rating_value').html($('#myRange').val());
    })


    $("#recommended_books").on('click','.give_rating',function (event) {
        $('#success-alert').hide()
        var isbn = $(this).text();
        current_isbn = isbn;
    })
   $("#browse_books").on('click','.give_rating',function (event) {
       $('#success-alert').hide()
        var isbn = $(this).text();
        current_isbn = isbn;
    })
   $("#trending_books").on('click','.give_rating',function (event) {
       $('#success-alert').hide()
        var isbn = $(this).text();
        current_isbn = isbn;
    })
    // submit rating button inside modal
    $('#submit_rating').on('click', function () {
        var rating_value = $('#myRange').val()
        $.ajax({
            data:{userID: current_userID ,
                  ISBN: current_isbn,
                  rating_value: rating_value},
            type: 'POST',
            url: '/submit_rating'
        }).done(function (data) {
            if(data.error) {
                $('#fail-alert').show()
            }
            else if (current_page =='trending'){
                $('#success-activate-alert').show()
                //Update the trending page
            }
            else{
                $('#success-activate-alert').hide()
                $('#success-alert').show()
                $('div#recommended_books').empty().append(data.recommended_books)
                $('#history_books').empty().append(data.history_books)
                $('#browse_books').empty().append(data.browse_books)
                number_books_rated = number_books_rated + 1
            }

        })
    })

    //button to add new user
    $('#add_new_user').on('click',  function () {
        current_page = 'trending'
        $.ajax({
            type: 'GET',
            url: '/add_user'
        }).done(function (data) {
            trending_books_tally = trending_books_tally + 8
            current_userID = data.new_userID
            $('#home').hide()
            $('#main_list').hide()
            $('#book_shelf').show()
            $('#trending_books').empty().append(data.datax).show()
            $('#new_user_id').text(current_userID)


            $('#page_type').text('Welcome to BOOKIFY user ' +current_userID + '.')
            $('#page_type2').text('These are some highly popular books in the website.')
            $('#page_type_info').text('To activate this user account please rate 1 or more books.')
            $('#main_list2').show()


        })
    })

    $('#l_0').on('click' , function () {
        $.ajax({
            data:{'trending_books_tally':trending_books_tally},
            type: 'POST',
            url: '/get_trending'
        }).done(function (data) {
            $('#trending_books').empty().append(data.datax).show()
            trending_books_tally = trending_books_tally + 8
        })
    })





});

