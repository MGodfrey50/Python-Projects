# import urllib.request
import urllib

def connected(host='https://www.google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False

# test
# print( 'connected' if connected() else 'no internet!' )
if connected():
    print("Connected")
else:
    print("Not working")
    

