# #Set up

# In[1]:


import pandas as pd 
import numpy as np
from scipy.sparse.linalg import svds




# #Loading Book and Rating Table
#
#

# In[3]:


root_dir = '/Users/sandeep/Desktop/Homework2019/WebtechHomework/Webtech/flaskblog/BookData'
ratings_df = pd.read_csv(root_dir + '/ratev3_table.csv', sep=',', error_bad_lines=False,encoding="latin-1")
books_df = pd.read_csv(root_dir + '/books_table.csv',sep=',', error_bad_lines=False,encoding="latin-1")




# #Setting up Rating Data
#  - Formate rating matrix 
#     - user x movies 
#     - use df.piviot ffunction
#     - Fill cells with na with 0
# - De-mean the data
#     - nomrmalize by each users mean
#         - find mean vector: user_mean * 1 
#         - Subtract it from coloum
#     - Convert it form a dataframe to numpy array

# In[6]:


r_df = ratings_df.pivot(index='userID',columns='ISBN',values='bookRating').fillna(0)




# In[8]:


R = r_df.as_matrix()
users_mean_rating = np.mean(R, axis = 1)
R_demeaned = R - users_mean_rating.reshape(-1,1)


# #Singular Value Decomposition SVD
# - Follow the guide
# - Y = U x sigma x Vt
#     - Kinda like X x Theta'
#     - simga is a diagonal matrix like,identity matrix but not really
#         - Just scales things up
# 
# - Y = user X movie

# In[9]:


U,sigma,Vt = svds(R_demeaned, k=50)
sigma = np.diag(sigma)
Y = np.dot(np.dot(U,sigma),Vt) + users_mean_rating.reshape(-1,1)


# In[10]:


Y_df = pd.DataFrame(Y,columns = r_df.columns)


# In[11]:


Y_df.head()


# #Movie Reccomendation
#  - Build a function that take userID and return you the sorted_user_prediction
#     - Find which row the user is in?
#          - I have made the dataset such that userID == row_index
# 

# In[12]:


def get_sorted_user_prediction(userId):
  user_row_number = userId 
  sorted_user_pred = Y_df.iloc[user_row_number].sort_values(ascending = False)
  return sorted_user_pred


# In[14]:


def get_user_rated_books(books_dfx,ratings_dfx,userID):
  user_data = ratings_dfx[ratings_dfx.userID ==userID]
  user_full= user_data.merge(books_dfx,how='left',left_on = 'ISBN',right_on = 'ISBN').sort_values(['bookRating'],ascending=False)
  return user_full


# In[15]:


def get_recommendation(books_df, ratings_df , userID):
  user_rated_books = get_user_rated_books(books_df,ratings_df,userID)
  books_not_rated_by_user = books_df[~books_df['ISBN'].isin(user_rated_books['ISBN'])]
  
  sorted_books_prediction_score_for_user = get_sorted_user_prediction(userID);
  sorted_books_prediction_score_for_user= pd.DataFrame(sorted_books_prediction_score_for_user).reset_index()
  highest_scored_unseen_books=(books_not_rated_by_user.merge(sorted_books_prediction_score_for_user,how='left',
                                                            left_on = 'ISBN',right_on = 'ISBN'));

  highest_scored_unseen_books = highest_scored_unseen_books.rename(columns={userID:'Prediction'}).sort_values('Prediction',ascending = False).iloc[:10, :-1]

  return user_rated_books , highest_scored_unseen_books


# #Redo SVD

# In[19]:


def redo_SVD():
    global U,sigma,Vt,Y,Y_df
    U,sigma,Vt = svds(R_demeaned, k=50)
    sigma = np.diag(sigma)
    Y = np.dot(np.dot(U,sigma),Vt) + users_mean_rating.reshape(-1,1)
    Y_df = pd.DataFrame(Y,columns = r_df.columns)


# #Get Random unseen books

# In[20]:


def get_random_unseen_books(userID):
    books_df,ratings_df = get_df()
    user_rated_books = get_user_rated_books(books_df,ratings_df,userID)
    books_not_rated_by_user = books_df[~books_df['ISBN'].isin(user_rated_books['ISBN'])]
    return books_not_rated_by_user
    
    


# #Return dataframes
# 
# - book dataframe: books_df (named as)
# - ratings dataframe: ratings_df (named as)
#     - The changes that happens
#         - ratings_df -> r_df (pandas dataframe) -> R(numpy matrix)

# In[22]:


def get_df():
    return books_df, ratings_df


# #Post books, ratings, new_users
#     - Posting books and rating is easy
#          - Just append it to dataframe
#          - How does the book and rating obj look like?
#              - book_obj = {'ISBN':.. , 'book_title':.. , 'genre': ..}
#              - rating_obj = {'userID':.. , 'ISBN':.. , 'bookRating':..}
#     - Positng new_user
#         - What does it mean to post a new user?
#                - To do this prepare a list of objs
#                    - new_rating obj's for that user
#                        - {userID: XXX, ISBN: XXX , bookRating: XXX}
#                            - PLEASE MAKE SURE each KEY has right datatype
#                            - How to prepare values of each key is not this modules problem
#                - append each obj to rating dataframe
#                    

# In[23]:


def post_books(book_obj):
    print('hello')
    global books_df
    books_df = books_df.append(book_obj,ignore_index=True)


# In[24]:


def post_book_rating(rating_obj):
    global ratings_df,r_df,R,users_mean_rating,R_demeaned
    userID = int(rating_obj['userID'])
    isbn  = rating_obj['ISBN']
    bookRating = rating_obj['bookRating']
    print('ISBN  received:'+isbn)
    if len(ratings_df.loc[(ratings_df.userID == userID)&(ratings_df.ISBN == isbn)]) == 0:
        ratings_df = ratings_df.append(rating_obj , ignore_index=True)
    else:
        ratings_df.loc[(ratings_df.userID == userID)&(ratings_df.ISBN == isbn) , 'bookRating'] =bookRating
    
    #     remake  the r_df and r_demeaned
    r_df = ratings_df.pivot(index='userID',columns='ISBN',values='bookRating').fillna(0)
    R = r_df.as_matrix()
    users_mean_rating = np.mean(R, axis = 1)
    R_demeaned = R - users_mean_rating.reshape(-1,1)


# In[25]:


def post_new_users(rating_objs_list):
    for obj in rating_objs_list:
        ratings_df = ratings_df.append(obj, ignore_index=True)


# In[26]:


def get_new_book_isbn():
    new_book_isbn = max(books_df.index.unique()) +1 
    return str(new_book_isbn)
    
    


# #Delete book,book rating,user

# In[37]:


def delete_book_rating(rating_obj):
    userID = int(rating_obj['userID'])
    isbn  = rating_obj['ISBN']
    row_index = ratings_df.loc[(ratings_df.userID == userID)&(ratings_df.ISBN == isbn)].index
    ratings_df.drop(ratings_df.index[[row_index]],inplace= True)
        
       
    # remake  the r_df and r_demeaned
    r_df = ratings_df.pivot(index='userID',columns='ISBN',values='bookRating').fillna(0)
    R = r_df.as_matrix()
    users_mean_rating = np.mean(R, axis = 1)
    R_demeaned = R - users_mean_rating.reshape(-1,1)


# In[38]:


def check_isbn(isbn):
    global books_df
    if len(books_df[books_df.ISBN == isbn]) != 0:
        return True 
    else:
        return False


# In[39]:


def delete_book_bookify(isbn):
    global books_df,ratings_df
    books_df_row_index = books_df.loc[books_df.ISBN == isbn].index
    books_df.drop(books_df.index[[books_df_row_index]],inplace= True)
    
    if len(ratings_df[ratings_df.ISBN == isbn].index) != 0:
        ratings_df_row_index = ratings_df.loc[ratings_df.ISBN == isbn].index
        ratings_df.drop(ratings_df.index[[ratings_df_row_index]],inplace=True)


# In[40]:


def delete_user(userIDx):
    global ratings_df
    row_index = ratings_df.loc[(ratings_df.userID == userIDx)].index
    print(row_index)
    print(userIDx)
    ratings_df = ratings_df.drop(ratings_df.index[row_index])
    
    


# #Get next user id 
#  - get index 
#  - drop the row using index, inplace

# In[48]:


def get_next_userID():
    sorted_userID_list  = sorted(ratings_df.userID.unique())
    return sorted_userID_list[-1] + 1
    


# In[49]:


def check_userID(userID):
    all_number = all([letter.isdigit() for letter in userID ])
    sorted_userID_list  = sorted(ratings_df.userID.unique())
    if all_number == False:
        print('not everything is a numver')
        return False
    elif (int(userID) not in sorted_userID_list):
        print('not in list')
        return False
    else:
        return True


# #Get Trending Score
#     - 0.3*(average_rating) + 0.7(frequecny_of_user_who_the_book)
# How to find average_rating of book?
#     - Find total rating
#         - Get all the rows with only that isbn
#         - take the sum of the rating column
#     - Find total user
#         - This gives: frequecny_of_user_who_rated_the_book
#         - Get the numbers of coloumns 
#         
# Append it to a new data_frame
# 
# #Get Trending Table
#  - For all books in books_df
#      - Get trending_score
#  - get_user_rated_books 
#  - In trending_table keep only books that are not in the user rated books
#      - User_rated_books['ISBN'] and trending_table['ISBN]
#      - But the userID is for the new user, user wont have rated any books at this stage
#          - Dont neeed userID 
#  - Return the table
# 
# #Get Trending Books
#     - return books_df
#         - sorted by the order in  trending_books ISBN

# In[54]:


def get_trending_score(isbn):
    global ratings_df
    book_ratings = ratings_df[ratings_df.ISBN == isbn]
    total_unique_users = len(book_ratings['userID'].unique())
    
    total_rating = book_ratings['bookRating'].sum()
    average_rating = total_rating/total_unique_users
    
    trending_score = 0.3*average_rating + 0.7*total_unique_users
    
    return trending_score
    


# In[55]:


def get_trending_table():
    global books_df
    global ratings_df
    ISBN_list = books_df['ISBN']
    trending_table = []
    for row in range(len(ISBN_list)):
        if row in ISBN_list:
            isbn = ISBN_list[row]
            trending_score = get_trending_score(isbn)
            data = {'ISBN':isbn, 'trending_score':trending_score}
            trending_table.append(data)
    trending_table = pd.DataFrame(trending_table)
    trending_table.sort_values('trending_score', ascending=False,inplace=True)
    
    #get all the highest trending books that user has not rated
#     trending_table = trending_table[~trending_table['ISBN'].isin(user_rated_books['ISBN'])]
    return trending_table
        
 


# In[56]:


def get_trending_books():
    trending_table = get_trending_table()
    books_df_copy =books_df.copy()
    books_df_copy = books_df_copy.set_index('ISBN')
    books_df_copy = books_df_copy.reindex(index=trending_table['ISBN'])
    books_df_copy = books_df_copy.reset_index()
    return books_df_copy
    
    

