import requests
from bs4 import BeautifulSoup
import pandas 

headers = {
	'user-agent': 'Mozilla/70.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
}
place_info  = input("Enter the place where you want to search for oyo:  ")
oyo_url = "https://www.oyorooms.com/hotels-in-{}/?page=".format(place_info)
page_num_MAX = int(input("Enter the number of pages to be scraped : "))
scraped_list_info = []
for page_num in range(1,page_num_MAX):
    
    req = requests.get(url=oyo_url+str(page_num), verify=True, headers=headers)
    content = req.content
    soup = BeautifulSoup(content,"html.parser")
    all_hotels = soup.find_all("div",{"class":"hotelCardListing"})

    for hotel in all_hotels:
        hotel_dict = {}
        hotel_dict["name"]  = hotel.find("h3",{"class":"listingHotelDescription__hotelName"}).text
        hotel_dict["address"]  = hotel.find("span",{"class":"u-line--clamp-2"}).text
        try:
            hotel_dict["price"] = hotel.find("span",{"class":"listingPrice__finalPrice"}).text
            hotel_dict["rating"]  = hotel.find("span",{"class":"hotelRating__ratingSummary"}).text
            parent_amenities_element = hotel.find("div",{"class":"amenityWrapper"})
            amenities_list = []
            for amenity in parent_amenities_element.find_all("div",{"class":"amenityWrapper__amenity"}):
                amenities_list.append(amenity.find("span",{"class":"d-body-sm d-textEllipsis"}).text.strip())
            hotel_dict["amenities"] = ', '.join(amenities_list[:-1])
        
        except AttributeError:
            pass
        scraped_list_info.append(hotel_dict)
dataFrame =  pandas.DataFrame(scraped_list_info)
dataFrame.to_csv("OyoScrapedInfo.csv")\