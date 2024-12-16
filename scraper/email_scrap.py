import httpx
from bs4 import BeautifulSoup
import re



def scrape_email(link: str):
    try:
        page_response = httpx.get(url=link)
        page_response.raise_for_status()
        # todo: check for status if failed return
        soup = BeautifulSoup(page_response.text, "html.parser")

        email_links = soup.findAll("a", attrs={"href": re.compile("^mailto:")})
        if not email_links:
            protected_elements = soup.findAll("span", {"class": "__cf_email__"})
            print(f'protected email: {link}')

        for link in email_links:
            # Extract the email address from the href attribute
            email = link.get("href").replace("mailto:", "")
    except Exception as e:
        print(f"An error occurred for {link}: {e}")
        email = None
    
    return email



def scrape_emails(links: list):
    emails = {}
    for link in links:
        # Send a GET request to each company page
        print(link)
        page_response = httpx.get(url=link)
        soup = BeautifulSoup(page_response.text, "html.parser")

        # print(soup)
        # pprint(soup.prettify())

        # contact_elements = soup.find_all(
        #     lambda tag: tag.name in ["a", "button"] and tag.get_text(strip=True).lower().find("contact") != -1
        # )
        # contact_elements = soup.find_all(lambda tag: tag.name in ["a", "button"] and "contact" in tag.get_text(strip=True).lower())
        contact_links = soup.find_all('a')
        for contact_link in contact_links:
            if 'contact' in contact_link.get_text(strip=True).lower():
                # print(contact_link)
                pass
                # contact_links.append(link)
        # if contact_elements:
        #     print('*')

        # Extract the company name from the HTML
        # company_name = soup.select_one("h1.dockable.business-name").text
        # Find all a tags with href that contain (mailto:) text
        email_links = soup.findAll("a", attrs={"href": re.compile("^mailto:")})
        # print(email_links)
        # break
        if not email_links:
            protected_elements = soup.findAll("span", {"class": "__cf_email__"})
            print('protected email')
        for link in email_links:
            # Extract the email address from the href attribute
            email = link.get("href").replace("mailto:", "")
            # Check if the company name exists in the emails dictionary and add it if not
            # if company_name not in emails:
            #     emails[company_name] = []
            print(email)
            # emails["a"].append(email)
        print("------------------------------------")            

    return emails
