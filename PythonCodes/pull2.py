import urllib.request
import ssl

# this is the workaround for the SSL certificate error
context = ssl._create_unverified_context()

# fetch content
def pull(url):
    # fetch the content
    response = urllib.request.urlopen(url, context=context).read()
    # decode the content
    text = response.decode('utf-8')
    # return the content
    return text

urlpath='https://www.bu.edu/academics/cas/courses/2/'

#pull path from urlpath
print(pull(urlpath))