from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import json
import csv
import datetime

url = "https://www.28hse.com/en/rent/residential"

# insert timestamp into csv file name
now = datetime.datetime.now()
timestamp = now.strftime("%Y%m%d%H%M%S")
csv_file_path = f"lease_price_{timestamp}.csv"

with open(csv_file_path, "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    # write header row
    writer.writerow(["District Area", "Gross Area", "Saleable Area", "Lease Price", "Page Number"])


def remove_comma(str) -> str:
    return str.replace(",", "")

def get_area(area_str: str) -> int:
    # Gross and saleable area are in the format of "Gross Area: 1234 sqft @45.3"
    # We need to extract the numeric value from the string
    # After split, the numeric value is the third element in the list
    # e.g. "Gross Area: 1234 sqft @45" -> ["Gross", "Area:", "1234", "sqft", "@45"]
    # Some of the area are written with comma e.g. "1,234 sqft", so we need to remove the comma
    area_str = remove_comma(area_str.split(" ")[2])
    return int(area_str)

def get_lease_price(lease_price_str: str) -> int:
    # remove HKD$ and comma
    lease_price_str = remove_comma(lease_price_str.replace("HKD$", ""))
    return int(lease_price_str)


def extract_page(page_num: int):
    # convert page_num to string
    page_num = str(page_num)
    search_url = "https://www.28hse.com/en/property/dosearch"
    form_data = {
        'page': page_num,
        'searchText': '',
        'myfav': '',
        'myvisited': '',
        'item_ids': '',
        'sortBy': '',
        'is_grid_mode': '',
        'search_words_thing': 'default',
        'buyRent': 'rent',
        'mobilePageChannel': 'residential',
        'cat_ids': '',
        'search_words_value': '',
        'is_return_newmenu': '0',
        'plan_id': '',
        'propertyDoSearchVersion': '2.0',
        'sortBy': 'default',
        'locations': '',
        'locations_by_text': '0',
        'mainType': '5',
        'mainType_by_text': '0',
        'otherRentalShortCut': '',
        'otherRentalShortCut_by_text': '0',
        'price': '',
        'price_by_text': '0',
        'areaOption': '',
        'areaOption_by_text': '0',
        'areaRange': '',
        'areaRange_by_text': '0',
        'roomRange': '',
        'roomRange_by_text': '0',
        'searchTags': '',
        'searchTags_by_text': '0',
        'others': '',
        'others_by_text': '0',
        'direction': '',
        'direction_by_text': '0',
        'landlordAgency': '',
        'landlordAgency_by_text': '0',
        'yearRange': '',
        'yearRange_by_text': '0',
        'floors': '',
        'floors_by_text': '0',
        'more_options': '',
        'more_options_by_text': '0'
        }
    encoded_form_data = urllib.parse.urlencode(form_data).encode('utf-8')
    request = urllib.request.Request(search_url, encoded_form_data, method='POST')
    response = urllib.request.urlopen(request)
    response_content = json.loads(response.read().decode('utf-8'))
    resultContentHTML = response_content['data']['results']['resultContentHtml']
    soup = BeautifulSoup(resultContentHTML, 'html.parser')
    with open('a.txt', 'w', encoding='utf-8') as output_file:
        # Property listing are contain in <div class="item property_item">
        properties = soup.find_all("div", class_="item property_item")

        # Loop through each property listing
        for property in properties:
            # District area is nested in <div class="district_area">
            district_area_parent_element = property.find("div", class_="district_area")
            # the first <a> element under <div class="district_area"> is the district area
            district_area = district_area_parent_element.find("a").get_text()
            print(district_area)

            # Gross and saleable area is nested in <div class="areaUnitPrice">
            # the first <div> element under <div class="areaUnitPrice"> is the gross area
            # the second <div> element under <div class="areaUnitPrice"> is the saleable area
            area_unit_price = property.find("div", class_="areaUnitPrice")
            gross_and_saleable_area = area_unit_price.find_all("div")
            gross_area = None
            saleable_area = None

            # Gross and saleable area are not always available
            # So we need to check if the area is available before extracting the area
            # There will always be two <div> elements under <div class="areaUnitPrice">, 
            # but need to check if there is text in the <div> element
            if gross_and_saleable_area[0].get_text().strip().split(" ")[0] == "Gross":
                gross_area_str = gross_and_saleable_area[0].get_text().strip()
                gross_area = get_area(gross_area_str)
            if gross_and_saleable_area[1].get_text().strip().split(" ")[0] == "Saleable":
                saleable_area_str = gross_and_saleable_area[1].get_text().strip()
                saleable_area = get_area(saleable_area_str)

            print(gross_area)
            print(saleable_area)

            # Lease Price is nested in <div class="extra">
            extra_info = property.find("div", class_="extra")
            # Lease price is written in <div class="ui right floated green large label">
            lease_price_element = extra_info.find("div", class_="ui right floated green large label")
            if lease_price_element is None:
                lease_price_element = extra_info.find("div", class_="ui right floated large label")
            lease_price_str = lease_price_element.get_text()
 

            # lease price is in the format of "HKD$123,456"
            # We need to extract the numeric value from the string
            # After split, the numeric value is the second element in the list
            # e.g. "HKD$123,456" -> ["HKD$123,456"] -> ["HKD$", "123,456"] -> "123,456"
            # Convert the numeric value to integer by removing the comma
            lease_price = get_lease_price(lease_price_str.strip().split(" ")[1])
            print(lease_price)

            with open(csv_file_path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([district_area, gross_area, saleable_area, lease_price, page_num])
            

if __name__ == "__main__":
    for i in range(1, 100):
        extract_page(i)