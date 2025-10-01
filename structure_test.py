

import requests
from rich import print 
from bs4 import BeautifulSoup


class Site:
    def __init__(self,site_name,title_html,price_html,desc_html):
        self.site_name = site_name
        self.title_html = title_html
        self.price_html = price_html
        self.desc_html  = price_html

    
roboShopBd = Site("robo","se","see","seff")

print(roboShopBd.title_html)
roboShopBd.title_html = "new"
print(roboShopBd.title_html)



# print(sites)

# for site in sites:
#     # print(site["name"])
#     pass

soup = BeautifulSoup("""


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>BeautifulSoup Practice</title>
</head>
<body>
    <h1>Welcome to BS4 Practice Page</h1>
    <p>This page contains various HTML elements for BeautifulSoup practice.</p>
    
    <h2>Tables</h2>
    <table id="table1">
        <tr>
            <th>Name</th><th>Age</th><th>City</th>
        </tr>
        <tr>
            <td>Alice</td><td>30</td><td>New York</td>
        </tr>
        <tr>
            <td>Bob</td><td>25</td><td>London</td>
        </tr>
    </table>
    <table id="table2">
        <tr>
            <th>Product</th><th>Price</th>
        </tr>
        <tr>
            <td class="product">Laptop</td><td class="price">$999</td>
        </tr>
        <tr>
            <td class="product">Phone</td><td class="price">$499</td>
        </tr>
    </table>
    
    <h2>Lists</h2>
    <ul>
        <li>Fruits
            <ul>
                <li class="product">Apple</li>
                <li class="product">Banana</li>
                <li class="product">Citrus
                    <ul>
                        <li>Orange</li>
                        <li>Lemon</li>
                    </ul>
                </li>
            </ul>
        </li>
        <li>Vegetables
            <ul>
                <li>Carrot</li>
                <li>Broccoli</li>
            </ul>
        </li>
    </ul>
    <ol>
        <li>Step 1</li>
        <li>Step 2
            <ol>
                <li>Substep 2.1</li>
                <li>Substep 2.2</li>
            </ol>
        </li>
        <li>Step 3</li>
    </ol>
    
    <h2>Links</h2>
    <a href="https://www.example.com" class="external">Example</a>
    <a href="/internal/page1" class="internal">Internal Page</a>
    <a href="https://www.github.com" class="external">GitHub</a>
    
    <h2>Other Elements</h2>
    <div id="info">
        <p class="desc">This is a description inside a div.</p>
        <span data-value="42">Special Value</span>
    </div>
    <form action="/submit" method="post">
        <input type="text" name="username" />
        <input type="password" name="password" />
        <button type="submit">Login</button>
    </form>
</body>
</html>
""", "html.parser")

print(soup.find_all(class_="product"))