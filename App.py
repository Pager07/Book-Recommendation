#!/usr/bin/env python
# coding: utf-8

# #Set Up

# In[1]:


from flask import Flask,render_template,url_for,request, jsonify
import pandas as pd
import sys 
import random
import json
import Database as database

app = Flask(__name__)


# #Svd module: GET USER RECOMMENDATION , USER RATED BOOKS , TRENDING BOOKS
# 

# - THIS FUNCTION RETURN A DICT WITH RECOMMENDATED RATING FOR  GIVEN USER
#     - user get_reommendation function()
#         - Takes in userID, books_df , rating_df
#         - How to get books_df, rating_df?
#             - HAVE A FUNCTION IN SVDHW THAT RETURNS THE 2 DATAFRAME
#             - THIS WILL BE THE ARGUMENTS 
#     - Retrun a dict
#         -{0: {'userID': 15,
#               'ISBN': '0840748493',
#               'bookRating': 8,
#               'book_title': 'Gift Of The Blessing, The',
#               'genre': 'Religion|Inspirational'},
#          1: { 'userID': 15,
#               'ISBN': '1591856132',
#               'bookRating': 8,
#               'book_title': 'Shadowmancer',
#               'genre': 'Magic|Fantasy'}}
#          - How to access it?
#              - dict['whatFeature/Col.eg.userID']['whatRow']
#              - kinda the opposite

# In[4]:


def get_user_recommendation(userID):
    books_df , ratings_df = database.get_df()
    user_rated_books, new_books =database.get_recommendation(books_df,
                                                             ratings_df,
                                                             userID)
    return new_books.to_dict('index')


# In[5]:


def get_user_rated_books(userID):
    books_df , ratings_df = database.get_df()
    user_rated_books, new_books =database.get_recommendation(books_df,
                                                             ratings_df,
                                                             userID)
    return user_rated_books.to_dict('index')


# In[6]:


def get_trending_books():
    trending_books = database.get_trending_books()
    return trending_books.to_dict('index')
    


# #Svd module: Post NEW BOOKS, USER, USER RATING, NEW USER
# - New books
#     - A BOOK ROW OBJ LOOKS LIKE THIS
#          - {'ISBN': XXXX,  'book_title': , 'genre': }
#     - MAKE A FUNCTION IN database that takes a book obj and add its the data frame
#     

# In[7]:


def get_new_user_id():
    return database.get_next_userID()


# #Flask

# In[8]:


@app.route("/")
def home():
    return render_template('home.html')


# In[9]:


@app.route("/history", methods=['POST'])
def get_history_page():
    userID = int(request.form['userID'])
    rated_books = get_user_rated_books(userID)
    if len(rated_books) ==0 :
        data = jsonify({'error':'You have not rated any books.'})
    else:
        data = jsonify({'datax':render_template('history.html' , posts=rated_books)
                       })
    return data
    


# In[10]:


@app.route("/swap_user",methods = ['POST'])
def swap_user():
    userID = request.form['userID']
    exist = database.check_userID(userID)
    
    print(f'{exist},{userID}')
    if exist:
        template = render_template('recommend.html',
                                   data=get_user_recommendation(int(userID))
                                  )
    
        data = jsonify({'datax':template})
    else:
        data = jsonify({'error': 'UserID does not exist in the database'})
    return data


# In[11]:


@app.route("/browse",methods = ['POST'])
def browse(userID=None):
    server_requested = True
    if userID == None:
        userID = int(request.form['userID'])
        server_requested = False
    random_unseen_books = database.get_random_unseen_books(userID);
    random_unseen_books = random_unseen_books.to_dict('index');
    keys = list(random_unseen_books.keys())
    keys = keys[0:8] 
    random.shuffle(keys)
    data = {}
    for key in keys:
        data[key] = random_unseen_books[key]
    template = render_template('recommend.html', 
                              data = data )
    if server_requested:
        return template
    else:
        return jsonify({'datax':template})
    
    


# In[12]:


@app.route('/add_user', methods=['GET'])
def add_user():
    new_user_id = get_new_user_id()
    trending_books = get_trending_books()
    #top 8 trending books
    keys = list(trending_books.keys())
    data  = {}
    for key in keys[:8]:
        data[key] = trending_books[key]
    template = render_template('recommend.html', data=data)
    data = jsonify({'datax':template , 'new_userID':str(new_user_id) })
    return data
    


# In[13]:


@app.route('/get_trending', methods=['POST'])
def get_trending():
    print('Getting book tally..')
    number_books_already_sent = int(request.form['trending_books_tally'])
    print('Getting trending books..')
    trending_books = get_trending_books()
    print('Doing Rest..')
    keys = list(trending_books.keys())
    data  = {}
    for key in keys[number_books_already_sent:number_books_already_sent+8]:
        data[key] = trending_books[key]
    template = render_template('recommend.html', data=data)
    data = jsonify({'datax':template})
    print('Sending Trending books')
    return data
    


# In[14]:


@app.route("/submit_rating", methods=['POST'])
def submit_rating():
    
    print('Fetching userID..')
    
    userID = int(request.form['userID'])
    
    print('Fetching ISBN..')

    ISBN = request.form['ISBN']
    
    print('Fetching bookRating..')
    bookRating = int(request.form['rating_value'])
    
    print('Making  obj..')
    rating_obj = {'userID':userID,'ISBN':ISBN,'bookRating':bookRating}
    
    print('Posting books to database..')
    database.post_book_rating(rating_obj)
    print('Redoing SVD..')
    print(database.check_userID(str(userID)) )
    
    database.redo_SVD()
    
    exist = database.check_userID(str(userID))
    print(exist)
    if exist:
        template = render_template('recommend.html',
                                   data=get_user_recommendation(int(userID))
                                  )
        template2 = render_template('history.html' ,
                                    posts=get_user_rated_books(int(userID)))
        
        template3 = browse(userID= int(userID))
    
        data = jsonify({'recommended_books':template ,
                        'history_books':template2,
                        'browse_books':template3
                       })
    else:
        #then it must be new user trying to activate their account
        data = jsonify({'error': 'UserID does not exist in the database'})
    return data
    
    


# In[15]:


@app.route("/delete_book" , methods=['DELETE'])
def delete_book():
    print('Getting userId for deleting books')
    userID = int(request.form['userID'])
    print('Getting isbn for deleting book')
    isbn  = request.form['ISBN']
    rating_obj = {'userID':userID,'ISBN':isbn}
    print('Deleting book obj from database')
    database.delete_book_rating(rating_obj)
    print('Checking userID ')
    exist = database.check_userID(str(userID))
    
    database.redo_SVD()
    if exist:
        template2 = render_template('history.html' ,
                                    posts=get_user_rated_books(int(userID)))
    
        data = jsonify({
                        'history_books':template2,
                       })
    else:
        #then it must be new user trying to activate their account
        data = jsonify({'error': 'UserID does not exist in the database'})
    return data


# In[16]:


@app.route('/add_book',methods=['GET'])
def add_book():
    new_book_isbn = database.get_new_book_isbn()
    data = jsonify({'new_book_isbn':new_book_isbn})
    return data
    


# In[17]:


@app.route('/submit_new_book',methods=['POST'])
def submit_new_book():
    userID,bookRating = int(request.form['userID']),int(request.form['bookRating'])
    book_title, genre = request.form['book_title'] , request.form['genre']
    isbn = request.form['ISBN']
    
    rating_obj = {'userID':userID, 'ISBN':isbn,'bookRating':bookRating}
    book_obj  = {'ISBN':isbn,'book_title':book_title, 'genre':genre}
    
    database.post_book_rating(rating_obj)
    database.post_books(book_obj)
    
    database.redo_SVD()
    
    
    exist = database.check_userID(str(userID))
    print(exist)
    if exist:
        template = render_template('recommend.html',
                                   data=get_user_recommendation(int(userID))
                                  )
        template2 = render_template('history.html' ,
                                    posts=get_user_rated_books(int(userID)))
        
        template3 = browse(userID= int(userID))
    
        data = jsonify({'recommended_books':template ,
                        'history_books':template2,
                        'browse_books':template3
                       })
    else:
        #then it must be new user trying to activate their account
        data = jsonify({'error': 'UserID does not exist in the database'})
    return data
    


# In[18]:


@app.route('/delete_book_bookify' , methods=['DELETE'])
def delete_book_bookify():
    isbn = request.form['ISBN']
    exist = database.check_isbn(isbn)
    if exist:
        database.delete_book_bookify(isbn)
        return jsonify({'success':'Book deleted!'})
    else:
        return jsonify({'error':'ISBN DOES NOT EXIST'})
    


# In[19]:


@app.route('/delete_user',methods=['DELETE'])
def delete_user():
    userID = int(request.form['userID'])
    print('Recived userID:'+str(userID))
    database.delete_user(userID)
    return jsonify({'success':'User deleted!'})


# In[20]:


if __name__ == '__main__':
    app.run()

