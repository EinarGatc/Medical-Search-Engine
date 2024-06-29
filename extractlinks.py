import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
from Scraper import visitedUrls

# TO DO: create isValid function for extractLinks checks

def extractLinks(baseUrl, htmlString):
    newLinks = []

    soup = BeautifulSoup(htmlString, 'html.parser')
    for tag in soup.find_all('a'): 
      if tag.get('href'):
        newLink = tag['href']
        absoluteLink = createAbsoluteUrl(baseUrl, newLink)
        if absoluteLink not in visitedUrls and absoluteLink not in newLinks: 
          newLinks.append(absoluteLink)
        
    return newLinks
    
            
def createAbsoluteUrl(baseUrl, newUrl):
    newUrl = newUrl.split('#', 1)[0].strip().lower()
    absoluteUrl = urljoin(baseUrl, newUrl)
    absoluteUrl = normalize(absoluteUrl)

    return absoluteUrl

def normalize(url):
    """Normalize the URL by removing fragments and query parameters, lowercasing, etc."""
    parsed_url = urlparse(url)
    normalized_url = urlunparse((
        parsed_url.scheme,
        parsed_url.netloc.lower(),
        parsed_url.path.rstrip('/'),
        parsed_url.params,
        '',  
        ''  
    ))
    return normalized_url

def ExtractLinksUnitTesting():
  assert extractLinks("", "") == []
  assert extractLinks("", "<li><a href=\"https://www.example.com/blog\">Blog</a></li>") == ["https://www.example.com/blog"]
  assert extractLinks("", "<a href=\"https://www.example.com/blog\">") == ["https://www.example.com/blog"]
  assert extractLinks("https://www.example.com", "<li><a href=\"blog\">Blog</a></li>") == ["https://www.example.com/blog"]
  print("Passed all ExtractLinks Unit Tests")

def CreateAbsoluteUrlUnitTesting():
  assert createAbsoluteUrl("","") == ""
  assert createAbsoluteUrl("https://www.example.com", "blog") == "https://www.example.com/blog"
  assert createAbsoluteUrl("https://www.example.com", "https://www.webmd.com/blog") == "https://www.webmd.com/blog"
  print("Passed all CreateAbsoluteUrl Unit Tests")

def NormalizeUnitTesting():
  assert normalize("") == ""
  assert normalize("https://www.webmd.com/blog?") == "https://www.webmd.com/blog?" # should return the url with the query preserved
  print("Passed all Normalize Unit Tests")

'''
def extractLinks(baseUrl, htmlString):
1. make soup object
2. use soup object to find all anchor tags
    a. extract the href links connected to the anchor tags if:
        b. the link matches a valid domain (htmlString)
            c. the extracted link can be relative or absolute, so always convert it to an absolute link
            d. once converted to an absolute link, check if the absolute link matches a valid domain:
                e. if it does, then add the link (before converting to absolute) into our list of extracted links
                f. if it doesn't, add to set of visited links
3. return list of scraped links
'''


if __name__ == "__main__": 
  # Testing extraction
  ExtractLinksUnitTesting()
  CreateAbsoluteUrlUnitTesting()
  NormalizeUnitTesting()
  html_string = '''
      <html lang="en">
      <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Example Page</title>
      </head>
      <body>
          <header>
              <h1>Welcome to the Example Page</h1>
              <nav>
                  <ul>
                      <li><a href="index.html">Home</a></li>
                      <li><a href="about.html">About Us</a></li>
                      <li><a href="services.html">Services</a></li>
                      <li><a href="contact.html">Contact</a></li>
                      <li><a href="https://www.example.com/blog">Blog</a></li>
                  </ul>
              </nav>
          </header>

          <main>
              <section>
                  <h2>Our Mission</h2>
                  <p>Our mission is to provide the best services to our customers. Learn more <a href="about.html#mission">here</a>.</p>
                  <p>Visit our <a href="https://www.example.com">main website</a> for more information.</p>
              </section>

              <section>
                  <h2>Services</h2>
                  <ul>
                      <li><a href="services/web-development.html">Web Development</a></li>
                      <li><a href="services/mobile-apps.html">Mobile Apps</a></li>
                      <li><a href="services/digital-marketing.html">Digital Marketing</a></li>
                      <li><a href="https://www.example.com/services/consulting">Consulting</a></li>
                  </ul>
              </section>

              <section>
                  <h2>Contact Us</h2>
                  <p>For inquiries, please <a href="contact.html#form">fill out our contact form</a> or visit our <a href="https://www.example.com/contact">contact page</a>.</p>
                  <p>Email us at <a href="mailto:info@example.com">info@example.com</a></p>
                  <p>Call us at <a href="tel:+1234567890">+1 234 567 890</a></p>
              </section>
          </main>

          <footer>
              <p>&copy; 2024 Example Company. All rights reserved.</p>
              <p>Follow us on <a href="https://www.facebook.com/example">Facebook</a>, <a href="https://www.twitter.com/example">Twitter</a>, and <a href="https://www.linkedin.com/company/example">LinkedIn</a>.</p>
          </footer>
      </body>
      </html>
  '''
      
  base_url = "https://medlineplus.gov"
  newLinksExtracted = extractLinks(base_url, html_string) # extract all absolute links and relative links

  for link in newLinksExtracted:
      print(link)