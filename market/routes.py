from market import app , db , login_manager
from flask import render_template , redirect , url_for , flash ,request
from market.Models import Item , User
from market.forms import RegisterForm , LoginForm , PurchaseForm , SellForm
from flask_login import login_user , logout_user , login_required , current_user

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")
     
@app.route("/market", methods=["GET", "POST"])
@login_required
def market_page():
    purchase_form = PurchaseForm()
    selling_form = SellForm()
    if request.method == "POST": 
        # PURCHASE ITEM
        purchased_item = request.form.get('purchased_item')
        p_item_object =  Item.query.filter_by(name=purchased_item).first()
        if p_item_object: 
            if current_user.can_purchase(p_item_object):
                p_item_object.owner = current_user.id
                current_user.budget -= p_item_object.price
                db.session.commit()
                flash(f'Congratulations You Purchased {p_item_object.name}' 
                                                    , category='success')
            else:
                flash("You don't have enough credit" , category = 'danger')
        # SELL ITEM
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.owner = None
                current_user.budget += s_item_object.price
                db.session.commit()
                flash(f'Congratulations You Sold {p_item_object.name}' 
                                                    , category='success')
        return redirect(url_for('market_page'))
    if request.method == "GET":
            
        items = Item.query.filter_by(owner = None)
        owned_items = Item.query.filter_by(owner =current_user.id)
        return render_template('market.html', items=items , purchase_form =purchase_form 
                                , owned_items = owned_items , selling_form= selling_form)

@app.route("/register", methods= ['GET' , 'POST'])
def registeration_page():
    form = RegisterForm()
    if form.validate_on_submit():
        userr = User(username=form.username.data 
                    ,email_add = form.email_add.data  ,password=form.password1.data)
        db.session.add(userr)
        db.session.commit()
        login_user(userr)
        flash(f'Account created successfully,\nYou are logged in as :{userr.username}' 
              , category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}: 
        for error in form.errors.values() :
            flash(error , category='danger')
    return render_template('register.html' , form = form)   


@app.route("/login" , methods = ['GET' , 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        atemptted_user = User.query.filter_by(username=form.username.data).first()
        if atemptted_user and atemptted_user.check_password_correction(
                                attempted_password= form.password.data
        ):
            login_user(atemptted_user)
            flash(f'You are logged in as :{atemptted_user.username}' , category='success')
            return redirect(url_for('market_page'))
        else:
            flash("Wrong Username or Password" , category='danger')
    return render_template('login.html' , form = form)

@app.route("/logout" )
def logout_page():
    logout_user()
    flash("You have been logged out" , category='info')
    return redirect(url_for('home_page'))