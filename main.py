from twisted.web import http
import re
import sys
sources=re.compile('([ax]s(\.[0-9]*[1-9][0-9]*)?)$')
class MagnetHandler(http.Request):
    def sortedurls(self):
        allkeys=self.args.keys()
        urls=[]
        self.matchedkeys=[key for key in allkeys if sources.match(key)]
        self.matchedkeys.sort(lambda x,y:cmp(y[0],x[0]) or cmp(int('0'+x[3:]),int('0'+y[3:])))
        for mykey in self.matchedkeys:
            urls += self.args[mykey]
        return urls

    def processmagnet(self):
        urls=self.sortedurls()
        if len(urls) == 0:
            self.setResponseCode(http.NOT_FOUND)
            self.write("<h1>Not found<h1>Unable to find any usable URL/URN in the magnet URI\n")
            self.write('/'.join(self.matchedkeys))
        else:
            self.setHeader('Location',urls[0])
        if len(urls) > 1:
            self.setResponseCode(http.MULTIPLE_CHOICE)
            self.write("<h1>Alternate Locations</h1><ol>")
            for url in urls:
                self.write('<li><a href="'+url+'">'+url+'</a></li>')
            self.write("</ol>")
        elif len(urls) == 1:
            self.setResponseCode(http.TEMPORARY_REDIRECT)

    def process(self):
        if self.path == "/magnet:":
            self.processmagnet()
        else:
            self.setResponseCode(http.NOT_FOUND)
            self.write("<h1>Not found</h1>Unable to retrieve page\n")
        self.finish()

class MagnetHTTPChannel(http.HTTPChannel):
    requestFactory=MagnetHandler

class MagnetHTTPFactory(http.HTTPFactory):
	protocol=MagnetHTTPChannel

if __name__ == "__main__":
    from twisted.internet import reactor
    reactor.listenTCP(8080, MagnetHTTPFactory())
    reactor.run()

