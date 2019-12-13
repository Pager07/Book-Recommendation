$(document).ready(function () {
    console.log('READY!')
    var current_userID;
    var current_isbn;
    var number_books_rated;
    var trending_books_tally = 0 ;
    var current_page = 'home';
    var next_new_book_isbn;
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
            $('#adding_book').hide()
            $('#delete_bookify_book').hide()
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
            $('#adding_book').hide()
            $('#delete_bookify_book').hide()
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
            $('#adding_book').hide()
            $('#delete_bookify_book').hide()
            $('#recommended_books').hide()
            $('#history_books').hide()
            $('#browse_books').empty().append(data.datax).show()
            $('#page_type').text('Explore and rate books:' + current_userID )
            $('#page_type_info').text('Click Browse agian to load new books')
            $('#l_2_1').show()
            $('#l_2_2').show()
        })
    })

    //    Adding book
    var set_next_new_book_isbn = function(){
         $.ajax({
            type: 'GET',
            url: '/add_book'
        }).done(function (data) {
            next_new_book_isbn = data.new_book_isbn
        })
    }
    $('.add_book').on('click', function () {
        $('#add-book-success-alert').hide()
        $('#add-book-fail-alert').hide()
        $('#recommended_books').hide()
        $('#delete_bookify_book').hide()
        $('#trending_books').hide()
        $('#history_books').hide()
        $('#browse_books').hide()
        $('#delete_bookify_book').hide()
        $('#adding_book').show()
        set_next_new_book_isbn()
        $('#page_type').text('Add books user:' + current_userID )
        $('#page_type_info').text('The system will give the new book bookID/ISBN:'+ next_new_book_isbn)
        $('#l_2_1').show()
        $('#l_2_2').show()
    })
    $('#add_book_btn2').on('click', function (event) {
        event.preventDefault();
        var error = 1
        var new_book_title = $('#new_book_title').val()
        var new_book_genre_list = $("#new_book_genres").tagsinput('items')
        var rating_value = $('#myRange2').val()
        var genre_str = ''
        if(new_book_genre_list.length >=1){
            error = 0
            new_book_genre_list.forEach(function (item,index) {
                if(index != 0){
                    genre_str = genre_str+'|'+item
                }else{
                    genre_str = genre_str + item
                }
            })
        }
        if(new_book_title.length < 1){
            error = 1
        }
        if(error == 0){
            var rating_obj = {'userID':current_userID, 'ISBN':next_new_book_isbn,'bookRating':rating_value}
            var book_obj = {'ISBN':next_new_book_isbn,'book_title':new_book_title, 'genre':genre_str}
            $.ajax({
                data: {userID:current_userID,
                       ISBN:next_new_book_isbn,
                        bookRating: rating_value,
                        genre: genre_str,
                        book_title: new_book_title},
                type: 'POST',
                url: '/submit_new_book'
            }).done(function (data) {
                $('#add-book-fail-alert').hide()
                $('#add-book-success-alert').show()
                $('div#recommended_books').empty().append(data.recommended_books)
                $('#history_books').empty().append(data.history_books)
                $('#browse_books').empty().append(data.browse_books)
                number_books_rated = number_books_rated + 1
            })
        }else{
            $('#add-book-success-alert').hide()
            $('#add-book-fail-alert').show()
        }

    })
    //Delete Book From Bookify
   $('.delete_book_bookify').on('click',function () {
        $('#delete-book-bookify-fail-alert').hide()
        $('#delete-book-bookify-success-alert').hide()
        $('#recommended_books').hide()
        $('#history_books').hide()
        $('#browse_books').hide()
        $('#adding_book').hide()
        $('#trending_books').hide()
        $('#delete_bookify_book').show()
        $('#page_type').text('Delete books user:' + current_userID )
        $('#page_type_info').text('The system will remove the given ISBN')
        $('#l_2_1').show()
        $('#l_2_2').show()
    })
    $('#delete_book_bookify_btn').on('click', function () {
        var isbn = $('#delete_book_bookify_isbn').val()
        $.ajax({
            data:{ISBN:isbn},
            url:'/delete_book_bookify',
            type: 'DELETE'
        }).done(function (data) {
            if(data.error){
                $('#delete-book-bookify-fail-alert').show()
            }else{
                $('#delete-book-bookify-success-alert').show()
            }
        })
    })

    $('.log_out').on('click' , function () {
        $('#home').show()
        $('#recommended_books').empty()
        $('#history_books').empty()
        $('#browse_books').empty()
        $('#adding_book').hide()
        $('#delete_bookify_book').hide()
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

    $('#myRange2').on('input',function () {
        $('#rating_value2').html($('#myRange2').val());
    })

    $("#recommended_books").on('click','.give_rating',function (event) {
        $('#success-alert').hide()
        var isbn = $(this).text();
        current_isbn = isbn;
    })
    $("#history_books").on('click','.give_rating',function (event) {
        $('#success-alert').hide()
        var isbn = $(this).closest('.media-body').find('.history_isbn').text();
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
    $("#history_books").on('click','.delete',function (event) {
       $('#success-alert').hide()
        $('#success-delete-alert').hide()
        var isbn = $(this).closest('.media-body').find('.history_isbn').text();
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
         $('#trending_wait').show()
        $.ajax({
            data:{'trending_books_tally':trending_books_tally},
            type: 'POST',
            url: '/get_trending'
        }).done(function (data) {
            $('#trending_wait').hide()
            $('#trending_books').empty().append(data.datax).show()
            trending_books_tally = trending_books_tally + 8
        })
    })

    $('#delete_book').on('click' , function () {
        $.ajax({
            data: {'userID':current_userID, 'ISBN':current_isbn},
            type: 'DELETE',
            url: '/delete_book'
        }).done(function (data) {
            $('#success-delete-alert').show()
            $('#history_books').empty().append(data.history_books).show()
        })
    })






});

