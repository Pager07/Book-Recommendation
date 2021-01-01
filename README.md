## Book Recommendation using Singular Value Decomposition(SVD) ##

This is a recommendation system which is based on Singular Value Decomposition (SVD). Where SVD is applied to the rating matrix. It factorizes the rating matrix into 3 different matrix U, Sigma, Vt. The dot product of the 3 matrices is then taken in the following order (U)*Sigma*Vt to generate a user-profile matrix of size (number_of_users x number_of_books). A row in the user-profile matrix represents correlation/likability scores between a user and the movies.

![](./images/demo.gif)

## Objective of the project ## 
- [x] Generate user profile, AKA table of shape (number_of_user x number_of_books) using SVD
- [x] Use user-profile matrix to provide book recommendation based on a suitable
recommendation algorithm
- [x] Provide a suitable interface for a user to interact with the system, supporting user
profile creation and/or update and receiving book recommendations

## HOW TO RUN THE RECOMENDED SYSTEM ##

    IN Database.py change the following variable:
        - root_dir: TO PATH OF THE BookData Folder

    RUN THE App.py file:
        - python App.py



## Notes ## 
To generate the recommended book list, the system picks the books that have not been rated by the user and have the highest correlation scores. 

The system uses AJAX and has the ability to dynamically update. It provides the following functionalities 
- POST: Book, New User
- UPDATE: Rating
- DELETE: Previously rated books, Books form the system as a whole, User
- GET: Recommendation, Browse New books, Previously rated books

When adding a new user to the system, the user is asked to rate 1 or more books from the  "trending book list" to avoid cold start problem. The trending book list is a  ordered and descending list, where each book is given a trending score. The trending score of book is obtained  using "average_rating_for_the_book" and "total_unique_users_who_rated_the_book" features:

 trending_Score = 0.3*average_rating_for_the_book + 0.6*total_unique_users_who_rated_the_book

 I have given the second feature more weight because it favours books that have previously captured border audience and their attention such that they have made an effort to give a rating to the book. It also suppresses books that have very high rating within a small range of people. For example, books with 1  user that rated 10(max rating). 
 Hence, trending scores represents the weighted taste of books for users on the site.



 ## Dataset ## 
[Goodbooks-10k: a new dataset for book recommendations](http://fastml.com/goodbooks-10k-a-new-dataset-for-book-recommendations/)
