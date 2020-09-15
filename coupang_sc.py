import requests
import re
from bs4 import BeautifulSoup
headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}

search_input = input("찾고자 하는 검색어를 입력하세요")


for page_num in range(1,6):
    # print(page_num,"페이지")
    url = f"https://www.coupang.com/np/search?q={search_input}&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page={page_num}&rocketAll=false&searchIndexingToken=1=4&backgroundColor="


    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text,"lxml")

    # print(res.text)

    items = soup.find_all("li",attrs={"class":re.compile("search-product")})
    for item in items:
        #광고상품제외

        ad_badge = item.find("span",attrs={"class":"ad-badge"})
        if ad_badge:
            # print(" 광고상품제외")
            continue

        name = item.find("div",attrs={"class":"name"}).get_text()
        price = item.find("strong",attrs={"class":"price-value"}).get_text()
        rate = item.find("em",attrs={"class":"rating"})
        if rate:
            rate = rate.get_text()
        else:
            # print("평점없는  상품입니다.")
            continue

        review = item.find("span",attrs={"class":"rating-total-count"})
        if review:
            review = review.get_text()
            review = review[1:-1]
        else:
            # print("평가가 없는 상품입니다.")
            continue
        link = item.find("a",attrs={"class":"search-product-link"})["href"]

        if float(rate) >= 0 and  int(review) >= 1:  #조건에 따른 추출
            print(f"제품명:{name}")
            print(f"가격:{price}")
            print(f"평점:{rate}점 ({review})")
            print("바로가기 {}".format("https://www.coupang.com" + link))

        