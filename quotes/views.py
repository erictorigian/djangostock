from django.shortcuts import render, redirect
import requests, json
from .models import Stock, AppLog
from .forms import StockForm
import datetime 
from django.contrib import messages

# Create your views here.

def home(request):
    if request.method == 'POST':
        ticker = request.POST['ticker']
        
        api_token = 'pk_41fae4672a7d48d289090804749c20ef'
        http_request = "https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=" + api_token
        api_request = requests.get(http_request)
        
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error"
            ticker = "Stock not found"

        return render(request, 'home.html', {'api': api} )

    else:
        return render(request, 'home.html', {'ticker': 'Please enter a symbol above'})

def portfolio(request):
    api_token = 'pk_41fae4672a7d48d289090804749c20ef'
    portfolio_prices = []
    total_value = 0
    
    stocks = Stock.objects.all().order_by('ticker')
    for stock in stocks:
        ticker = stock.ticker
        shares = stock.shares
        http_request = "https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=" + api_token
        api_request = requests.get(http_request)
        api = json.loads(api_request.content)
        value = shares * api["latestPrice"]
        total_value = total_value + value 
        
        portfolio_prices.append({'ticker': ticker, 
                                'company_name': api['companyName'],
                                'shares': shares, 
                                'price':api["latestPrice"], 
                                'value': value })
    
    return render(request, 'portfolio.html', {
        'portfolio_prices': portfolio_prices,
        'total_value': total_value,
    } )

def about(request):
    return render(request, 'about.html', {} )

def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock has been added"))
            return redirect('add_stock')
        else:
            messages.error(request, ("Error in the form"))
            return redirect('add_stock')
    else:
        stocks = Stock.objects.all().order_by('ticker')
        return render(request, 'add_stock.html', {'stocks': stocks} )

def applog(request):
    if request.method == 'POST':
        #save to the database
        comment = request.POST['comment']
        version = request.POST['version']
        updated = datetime.datetime.now()
        entry = AppLog(version = version, comment = comment, updated = updated )
        entry.save()
 
    entries = AppLog.objects.all().order_by( '-updated')
    return render(request, 'applog.html', { 'entries': entries} )

def delete_stock(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock has been deleted"))
    return redirect(add_stock)


