# The analytical report

## General description
The odinshop is a marketplace for cracked websites/machines. They sell very cheap access to the websites and machines which were cracked
probably by using bruteforce. The most popular types of items are: cpanel, shell, mailer. They sell so fast, that when you reload the first page, all items are sold already.

## Cpanel
Cpanel is admin dashboard for hosting websites. It allowd website administrators to manage website using web GUI.
I suggest the Cpanel access is leaked by malicious freelance webdevs, who want to get additional income.

## Shell
Shell is malicious software which gives attacker persistance in a website to do varius stuff, like RCE or dumping useful info. Usually they are written in PHP
and uploaded by exploiting misconfigurated software / or CVE.

## Mailer
Mailer is access to SMTP servers, which makes it possble to send spam emails, and dont get filtered if the mailing server is trusted by email platforms.

Odinshop has premium subscription which allows you to buy premium versions of all this stuff.

## Leaks
Other popular leak is database of phone numbers, which might be used for spamcalling. They also have "view proof" which allows us to validate the leak, and mark those numbers as leaked.

There are also different types of stuff sold on this marketplace, but those are insignificant compared to the ones I described.

## Why this website
This webiste does not show actual leak until you pay to the merchants. So the only useful stuff we can take from this website is OSINT analytics of trends.
Also we can get information about recent deals, which might help in investigations.

# What data I decided to scrape
I decided to scrape only the popular types of sellings I described above, except phone numbers as they don't provide much useful information except country + few leaked numbers.

## Cpanel
Cpanel has a lot of useful information like **Masked domain** (hs4.*****om.br),Country, ISP. We may heal the mask of domain by downloading the zone files from [ICANN](https://www.icann.org/resources/pages/zfa-2013-06-28-en), 
and find the actual compromized website. But this is out of the scope of this project. 

## Shell
Shells also provide the masked domains, so they can also be healed. Shells also show ```uname``` of installed shells:
```
Linux - PHP 5.6.40 Linux bakuaz1.dot.az 3.10.0-1160.71.1.el7.x86_64 #1 SMP Tue Jun 28 15:37:28 UTC 2022 x86_64
```
Hostnames of the machines give us hints of ISP of the VPS. Also, we know the php version and linux kernel version, which might also be useful.

## The trades
The marketplace is transparent about Seller's deals, and we can scrape them too. They provide the information about buyer's account id and the type of stuff he sold.

Also the marketplace has Seller's detail page which shows the total_sales in USD, rating, last_login which are also super useful for trends analytics.

# How the scraper works
The scraper works by sending the webpage's data to aiohttp server. It intercepts the AJAX requests and sends copy of the request to the aiohttp server.
It automatically detects the page its on, and sends only the suitable for scraping data. 

The script is supposed to be run on each page load, like content_scripts of webextensions or userscript of tampermonkey. Bur for simplicity you can run the script in devtools. For an example open the page where shells are sold, and run the script. The pagination of the table works by sending AJAX requests, they happen each time you go to other page.

I embedded the sample src/db.sqlite which has the scraped data. You can open it using online sqlite viewr or download sqlitebrowser.