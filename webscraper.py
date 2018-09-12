# stamp
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
# print(os.getcwd())

# https://www.amtamassage.org/findamassage/index.html

# open file containing 51 postal codes in US
postalCodes = open("/home/justin/Documents/Projects/Salesforce/postalCodes.txt", "r")

# open file to write in csv format
file = open("/home/justin/Documents/Projects/Salesforce/leads.csv", "w")
baseUrl = 'https://www.amtamassage.org/findamassage/results.html?q=&l='
# write headers for csv file
headers = "Name, Practices, Phone, Address\n"
file.write(headers)

# iterate through all states
for line in postalCodes:
    # print(line.strip())
    stateUrl = baseUrl + line.strip() + '&searchcat=famt&PageIndex='

    # grab html from url
    for i in range(1, 50):
        url = stateUrl + str(i) + '&PageSize=10'
        print(url)
        uClient = uReq(url)
        page_html = uClient.read()
        uClient.close()

        # html parse
        page_soup = soup(page_html, "html.parser")
        # print(page_soup)
        # grab all massage therapists from the page
        containers = page_soup.find_all("ul", {"class": "famt-results"})
        try:
            contain = containers[0]
            contain = contain.find_all("li")

            # iterate through all leads in the page
            for i in range(len(contain)):
                name = contain[i].span.img["alt"]
                practices = contain[i].find_all("span", {"class": "techniques"})[0].text
                practices = practices.replace(",", "|")
                contact = contain[i].find_all("span", {"class": "mute contact"})[0].text
                phone = contact[:13]
                address = "\"" + contact[16:] + "\""
                # compile all the fields for each lead, then write them to csv
                file.write(("%s, %s, %s, %s\n") %
                            (name, practices, phone, address))

            # leads.write(str(containers))
        except:
            print('Next State')
            break
file.close()
