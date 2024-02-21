import urllib.request
import ssl

# this is the workaround for the SSL certificate error
context = ssl._create_unverified_context()

# URL to the file
urls = [
    'https://onexi.org/catalog/m1a.html',
    'https://onexi.org/catalog/m1b.html',
]

# fetch content
def pull(url):
    # fetch the content
    response = urllib.request.urlopen(url, context=context).read()
    # decode the content
    text = response.decode('utf-8')
    # return the content
    return text

# save file
def store(data, file):
    f = open('data/' + file, 'w')
    f.write(data)
    f.close()
    print('File saved as ' + file)

# loop through the URLs
for url in urls:
    index = url.rfind('/') + 1
    data = pull(url)
    file = url[index:]
    print('Fetching ' + file)
    store(data, file)
    # pause for a random time