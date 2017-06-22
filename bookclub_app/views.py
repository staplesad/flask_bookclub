from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from bookclub_app import app, db, lm
from sqlalchemy import desc
from random import randint
from .forms import LoginForm, BookForm, ReviewForm, WishBookForm
from .models import User, Book, Review, Quote, WishBook, check_password
from .emails import new_book_notification, upcoming_notification
###LOGIN AND HOME ###################################
@app.route('/')
@app.route('/index')
def index():
    user = g.user
    if g.user is not None and g.user.is_authenticated:
        books = Book.query.order_by(desc(Book.due_date)).all()
        wbooks = WishBook.query.filter_by(user=current_user).all()
        quote = choose_quote()
        return render_template('index.html', title='Home', user=user,
                books=books, wbooks=wbooks, quote=quote)
    return app.send_static_file('index_signedout.html')

@app.route('/about')
def about():
    return app.send_static_file('about.html')
	
@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html', title='Sign Up')	
	
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/login', methods=['GET','POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        user = User.query.filter_by(nickname=form.username.data).first()
        if user is None:
            flash('Login details are incorrect.')
        else:
            if check_password(user.hashed_password, form.password.data):
                if 'remember_me' in session:
                    remember_me = session['remember_me']
                    session.pop('remember_me', None)
                login_user(user, remember = remember_me)
                return redirect(request.args.get('next') or url_for('index'))
            else:
                flash('Login details are incorrect.')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/add_book')
@login_required
def add_book_opt():
    return render_template('add_book.html', title='Add Book')

#######################################
##### BOOK SECTION ####################

@app.route('/book/<title>')
@login_required
def book(title):
    book = Book.query.filter_by(title=title).first()
    if book == None:
        flash('Book %s not found.' % title)
        return redirect(url_for('index'))
    reviews = Review.query.filter_by(book=book).all()
    return render_template('book.html', title=title, book=book, reviews=reviews)

@app.route('/book/<title>/delete', methods=['GET','POST'])
@login_required
def book_delete(title):
    book = Book.query.filter_by(title=title).first()
    if book == None:
        flash('Book %s not found.' % title)
        return redirect(url_for('index'))
    db.session.delete(book)
    db.session.commit()
    flash('Book %s has been deleted.' % title)
    return redirect(url_for('index'))

@app.route('/book', methods=['GET', 'POST'])
@login_required
def new_book():
    form=BookForm()
    quote1 = choose_quote()
    quote2 = choose_quote()
    quotes = [quote1, quote2]

    if form.validate_on_submit():
        book = Book(title=form.title.data, due_date=form.due_date.data,
                info=form.info.data,
                author=current_user)
        db.session.add(book)
        db.session.commit()
        flash('New book has been added!')
        if form.notify.data==True:
            users = User.query.all()
            recipients=[]
            for user in users:
                recipients.append(user.email)
            new_book_notification(book, recipients)
            flash('Notification sent.')
        return redirect(url_for('book', title=book.title))
    
    return render_template('new_book.html', title='Add a New Bookclub Book', form=form,
            quotes=quotes, length_chars=None)

@app.route('/book/<title>/edit', methods=['GET','POST'])
@login_required
def edit_book(title):
    book = Book.query.filter_by(title=title).first()
    form=BookForm()
    quote1 = choose_quote()
    quote2 = choose_quote()
    quotes = [quote1, quote2]
    
    if book == None:
        flash('Book %s not found.' % title)
        return redirect(url_for('index'))
    if form.validate_on_submit():
        book.title = form.title.data
        book.due_date = form.due_date.data
        book.info = form.info.data
        db.session.add(book)
        db.session.commit()
        flash('Changes have been saved.')
        return redirect(url_for('book', title=title))
    else:
        form.title.data=book.title
        form.due_date.data=book.due_date
        form.info.data = book.info
    form_len=len(form.info.data)
    return render_template('new_book.html', title='Edit Book: %s' %title, form=form,
            quotes=quotes, length_chars=form_len)

@app.route('/book/<title>/notifyall')
@login_required
def notify_all(title):
    book=Book.query.filter_by(title=title).first()
    if book==None:
        flash('Book %s not found.' % title)
        return redirect(url_for('index'))
    users = User.query.all()
    recipients=[]
    for user in users:
        recipients.append(user.email)
    upcoming_notification(book, recipients)
    flash('Notification sent.')
    return redirect(url_for('book', title=title))


#######################################
##########REVIEWS######################
@app.route('/book/<title>/review', methods=['GET','POST'])
@login_required
def new_review(title):
    form=ReviewForm()
    book=Book.query.filter_by(title=title).first()
    review=Review.query.filter_by(book=book).filter_by(author=current_user).first()
    quote1 = choose_quote()
    quote2 = choose_quote()
    quotes = [quote1, quote2]
    
    if book==None:
        flash('Book %s not found.' % title)
        return redirect(url_for('index'))
    if review!=None:
        flash('You already left a review.')
        return redirect(url_for('book', title=title))
    if form.validate_on_submit():
        review = Review(star=form.star.data, text=form.text.data, book=book, author=current_user)
        db.session.add(review)
        db.session.commit()
        flash('Review has been saved.')
        return redirect(url_for('book', title=title))
    return render_template('new_review.html', title='New Review for %s' %title,
            form=form, quotes=quotes, length_chars=None)

@app.route('/book/<title>/review/edit', methods=['GET','POST'])
@login_required
def edit_review(title):
    form=ReviewForm()
    book=Book.query.filter_by(title=title).first()
    review=Review.query.filter_by(book=book).filter_by(author=current_user).first()
    quote1 = choose_quote()
    quote2 = choose_quote()
    quotes = [quote1, quote2]
    
    if book==None:
        flash('Book %s not found.' % title)
        return redirect(url_for('index'))
    if review==None:
        flash('Review not found.')
        return redirect(url_for('index'))

    if form.validate_on_submit():
        review.star=form.star.data
        review.text=form.text.data
        db.session.add(review)
        db.session.commit()
        flash('Review has been updated.')
        return redirect(url_for('book', title=title))
    else:
        form.star.data=review.star
        form.text.data=review.text
    form_len=len(form.text.data)
    return render_template('new_review.html', title='Edit Review for %s' %
            title, form=form, quotes=quotes,length_chars=form_len)

@app.route('/book/<title>/review/delete', methods=['GET','POST'])
@login_required
def review_delete(title):
    book=Book.query.filter_by(title=title).first()
    review = Review.query.filter_by(book=book).filter_by(author=current_user).first()
    if review == None:
        flash('Review of %s not found.' % title)
        return redirect(url_for('index'))
    db.session.delete(review)
    db.session.commit()
    flash('Your review of  %s has been deleted.' % title)
    return redirect(url_for('book',title=title))

####### User wishlist ###################
@app.route('/wishlist', methods=['GET'])
@login_required
def wishlist():
    books = WishBook.query.filter_by(user=current_user).all()
    quote = choose_quote()
    return render_template('wishlist.html', title='My Reading List', user=current_user, books=books, quote=quote)


@app.route('/wishlist/new', methods=['GET','POST'])
@login_required
def add_wishbook():
    form=WishBookForm()
    if form.validate_on_submit():
        book = WishBook(title=form.title.data, author=form.author.data,
                info=form.info.data,
                user=current_user)
        db.session.add(book)
        db.session.commit()
        flash('New book has been added!')
        return redirect(url_for('index'))
#        return redirect(url_for('wishlist'))
    return render_template('new_wishbook.html', title='Add a New Reading List Book',
            form=form, length_chars=None)

@app.route('/wishlist/<title>/edit', methods=['GET', 'POST'])
@login_required
def edit_wishbook(title):
    book = WishBook.query.filter_by(user=current_user, title=title).first()
    form=WishBookForm()
    if book == None:
        flash('Book %s not found.' % title)
        return redirect(url_for('wishlist'))
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.info = form.info.data
        db.session.add(book)
        db.session.commit()
        flash('Changes have been saved.')
        return redirect(url_for('index'))
#        return redirect(url_for('wishlist'))
    else:
        form.title.data=book.title
        form.author.data=book.author
        form.info.data = book.info
    form_len = len(form.info.data)
    return render_template('new_wishbook.html', title='Edit Book: %s' %title,
            form=form, length_chars=form_len)

@app.route('/wishlist/<title>/delete', methods=['GET','POST'])
@login_required
def wbook_delete(title):
    book=WishBook.query.filter_by(user=current_user, title=title).first()
    if book == None:
        flash('Review of %s not found.' % title)
        return redirect(url_for('index'))
    db.session.delete(book)
    db.session.commit()
    flash('%s has been deleted.' % title)
    return redirect(url_for('index'))
    
####### Quote functions ##################
def choose_quote():
    total_quotes = Quote.query.count()
    random_quote = randint(1,total_quotes)
    quote = Quote.query.get(random_quote)
    return quote.quote_text


