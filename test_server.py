from BaseHTTPServer import BaseHTTPRequestHandler , HTTPServer
import cgi
class MyServer(HTTPServer):
    pass
##    Voici un serveur basic qui ne fait que utiliser Heriter la
##    class HTTPServer de python , cette serveur va nous permettre
##    de tester et de comprendre les notions du w3C sur le traitement
##    des requetes HTTP, depuis un client (Programme client.py), nous
##    allons lui envoyer deux formulaires l un ne contenant que des fields
##    (key, value), il faut nous affiche le formulaire sur la console.
##    L'autre formulaire que nous allons lui envoyer va contenir un
##    formulaire contenue une clef , valeur , mais cette fois ci nous
##    allons envoye un  fichier comme valeur , enfin le contenu
##    du fichier comme nous le specifie W3C.




class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
##    Notre handler
    def do_POST(self):
        form = cgi.FieldStorage(
          self.rfile,
          headers = self.headers,
          environ = {
            "REQUEST_METHOD": "POST" ,
            "CONTENT_TYPE" : self.headers['Content-Type']
          }
        )

        for key in form.keys():
           v = form.getlist(key)
           print v
        self.response(200, "OK")
        return


    def response(self,code, output):
        self.send_header("content-type", "text/plain")
        self.end_headers()
        self.wfile.write(output)
        return code


if __name__ == "__main__":
    server_address = ('', 32)
    server= MyServer(server_address, SimpleHTTPRequestHandler)
    print("Starting Http Server on %s %s", server_address)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        server.server_close()
        sys.exit(0)      

    
    
    
