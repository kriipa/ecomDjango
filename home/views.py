from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

class Base(View):
    views = {}


class Homeview(Base):
    def get(self, request):
        self.views['categories'] = Category.objects.all()
        self.views['brands'] = Brand.objects.all()
        self.views['sliders'] = Slider.objects.all()
        self.views['reviews'] = Review.objects.all()
        self.views['hots'] = Product.objects.filter(labels = 'hot')
        self.views['newprod'] = Product.objects.filter(labels = 'new')
        self.views['ads'] = Ad.objects.all()
        self.views['count_cart'] = Cart.objects.filter(username = request.user.username, checkout= False).count()

        return render(request, 'index.html', self.views)

class CategoryView(Base):
    def get(self, request, slug):
        cat_id = Category.objects.get(slug = slug).id
        self.views['cat_products'] = Product.objects.filter(category_id = cat_id)
        self.views['categories'] = Category.objects.all()
        self.views['brands'] = Brand.objects.all()
        self.views['sales'] = Product.objects.filter(labels = 'sale')
        self.views['count_cart'] = Cart.objects.filter(username = request.user.username, checkout= False).count()

        return render(request, 'category.html', self.views)
    
class BrandView(Base):
    def get(self, request, slug):
        brand_id = Brand.objects.get(slug = slug).id
        self.views['brand_products'] = Product.objects.filter(brand_id = brand_id)
        self.views['categories'] = Category.objects.all()
        self.views['brands'] = Brand.objects.all()
        self.views['sales'] = Product.objects.filter(labels = 'sale')
        self.views['count_cart'] = Cart.objects.filter(username = request.user.username, checkout= False).count()

        return render(request, 'brand.html', self.views)
    
class ProductDetail(Base):
    def get(self, request, slug):
        print(slug)
        self.views['product_detail'] = Product.objects.filter(slug = slug)
        product_category = Product.objects.get(slug = slug).category_id
        self.views['related_products'] = Product.objects.filter(category_id = product_category)
        self.views['count_cart'] = Cart.objects.filter(username = request.user.username, checkout= False).count()
        self.views['count_cart'] = Cart.objects.filter(username = request.user.username, checkout= False).count()
        self.views['product_reviews'] = ProductReview.objects.filter(slug = slug)

        return render(request, 'product-detail.html', self.views)
    

class SearchView(Base):
    def get(self, request):
        if request.method == 'GET':
            query = request.GET['query']
            if query != "":
                self.views['search_products'] = Product.objects.filter(name__icontains = query)
            else:
                redirect('/')
        
        self.views['categories'] = Category.objects.all()
        self.views['brands'] = Brand.objects.all()
        self.views['sales'] = Product.objects.filter(labels = 'sale')
        self.views['count_cart'] = Cart.objects.filter(username = request.user.username, checkout= False).count()

        return render(request, 'search.html', self.views)

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        
        if password == cpassword:
            if User.objects.filter(username = username).exists():
                messages.error(request, "The username already exists!")
                return redirect('/signup')
            
            elif User.objects.filter(email = email).exists():
                messages.error(request, "The email is already in use.")
                return redirect('/signup')
            
            else:
                data = User.objects.create_user(
                    first_name = f_name,
                    last_name = l_name,
                    email = email,
                    username = username,
                    password = password
                )
                data.save()
        else:
            messages.error(request, "Passwords does not match")
            return redirect('/signup')
    return render(request, 'signup.html')

class CartView(Base):
    def get(self, request):
        username = request.user.username
        self.views['my_cart'] = Cart.objects.filter(username = username)
        my_cart = Cart.objects.filter(username = username, checkout = False)

        s = 0
        for i in my_cart:
            s = s + i.total
        self.views['all_total'] =s
        delivery_charge = 100
        self.views['grand_total'] = s + delivery_charge
        self.views['count_cart'] = Cart.objects.filter(username = request.user.username, checkout= False).count()

        return render(request, 'cart.html', self.views)
    
def add_to_cart(request, slug): 
    username = request.user.username
    if Cart.objects.filter(username = username, slug = slug, checkout = False):
        price = Product.objects.get(slug = slug).price
        discounted_price = Product.objects.get(slug = slug).discounted_price
        quantity = Cart.objects.get(slug = slug).quantity
        quantity = quantity +1
        if discounted_price > 0:
            total = discounted_price * quantity
        else:
            total = price * quantity

            Cart.objects.filter(username = username, slug = slug, checkout = False).update(
                quantity = quantity,
                total = total
            )
            return redirect('/cart')
    else:
        price = Product.objects.get(slug = slug).price
        discounted_price = Product.objects.get(slug = slug).discounted_price
        quantity = 1
        if discounted_price > 0:
            total = discounted_price 
        else:
            total = price 
        data = Cart.objects.create(
            username = username,
            slug = slug,
            quantity = quantity,
            total = total,
            items = Product.objects.filter(slug = slug)[0]
        )
        data.save()
    return redirect('/cart')

def delete_cart(request, slug):
    username = request.user.username
    if Cart.objects.filter(slug = slug, username = username, checkout = False):
        Cart.objects.filter(slug = slug, username = username, checkout = False).delete()
    return redirect('/cart')

def reduce_cart(request, slug):
    username = request.user.username
    if Cart.objects.filter(username = username, slug = slug, checkout = False):
        price = Product.objects.get(slug = slug).price
        discounted_price = Product.objects.get(slug = slug).discounted_price
        quantity = Cart.objects.get(slug = slug).quantity
        if quantity > 1:
            quantity = quantity - 1
            if discounted_price > 0:
                total = discounted_price * quantity
            else:
                total = price * quantity

            Cart.objects.filter(username = username, slug = slug, checkout = False).update(
                quantity = quantity,
                total = total
            )
        return redirect('/cart')
    
def product_review(request, slug):
    if Product.objects.filter(slug = slug):
        if request.method == 'POST':
            username = request.user.username
            star = request.POST['star']
            comments = request.POST['comment']
            ProductReview.objects.create(
                username = username,
                slug = slug,
                star = star,
                comments = comments
            ).save()

    else:
        return redirect(f'/product/{slug}')
    return redirect(f'/product/{slug}')