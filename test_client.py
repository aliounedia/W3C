import httplib, mimetypes
class W3Client:
    def __init__(self):
        self.files_fields  ={}
        self.simple_fields ={}

    def __len__(self):
        return len(self.files_fields) + len(self.simple_fields)
    
    def add_field(self, key, value_or_file):
        ##la methode 'add_field' , permet d' ajouter une clef /valeur --
        ##un form-field  a notre client. La clef est naturellement un
        ##string et la valeur peu etre un soit un fichier ou simplement
        ##un string
        ##
         
        encoding = 'iso-8859-1'
        if hasattr(value_or_file,'read'):
           print value_or_file.name
                
           type = mimetypes.guess_type(
                       value_or_file.name)[0] \
                          or 'application/octet-stream'
           data, filename= value_or_file.read().encode(encoding),\
                     value_or_file.name

           print 'filename', filename
           print 'filedata', data
           
           self.files_fields[key]=\
                                (data, (filename,type))
           return 
        # Sinon , nous somme en presence d un formulaire tres simple
        # clef/valeur pas de fichier , cool , on  n a qu a le foutre
        # self.simple_fields


        self.simple_fields[key] = value_or_file


    def postMultipart(self):
        ##est la ou les choses interessantes vont venir , nous allons
        ##maintenant envoyer a 'test_server' notre formulaires --
        ##self.self.files_fields  et --   self.simple_fields.

        ##Comme W3 les stipule:
        ##<INPUT type="text" name="submit-name" value  ="Larry">
        ##
        ##correspond a
        ##
        ##Content-Disposition: form-data; name="submit-name"
        ##
        ##Larry

        # Creons une connection avec 'test_server'
        conn = httplib.HTTPConnection("localhost", "32")

        # Notre BOUNDARY

        BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$' 

        contentType = 'multipart/form-data; boundary=%s' % BOUNDARY
        headers = {'User-Agent': 'Mozilla/5.0',
                   'Content-Type': contentType}


        body = ""
        a= []
        CRLF = "\r\n"
        a_append  =a.append
        for key, value  in self.simple_fields.items():
            a_append('--' + BOUNDARY)
            a_append('Content-Disposition: form-data; name="%s"' % key)
            a_append('')
            a_append(value)
        for key, (data, (filename, type)) in self.files_fields.items():
            a_append('--' + BOUNDARY)
            a_append('Content-Disposition: form-data; name="%s"; filename="%s"' % (
                    key, filename))
            a_append('Content-Type: %s' % type)
            a_append('')
            a_append(data)
        # 
        a_append('--' + BOUNDARY + '--')
        a_append('')
        body = CRLF.join(a)

        print  body
        conn.request('POST', "http://localhost/", body.encode("iso-8859-1"), headers)
        response = conn.getresponse()
        conn.close()
        print  response.status, response.read()

if __name__=="__main__":
    w3c=  W3Client()
    w3c.add_field("nom", "Alioune Dia")
    w3c.add_field("fichier", open("data_alioune.txt"))

    # Avant denvoyer ca au serveur, verifie que le serveur est lance en tapant
    # python test_server.py
    # Si ca run , tu dois voir sur la console
    # ('Starting Http Server on %s %s', ('', 32))
    w3c.postMultipart()

      

    


    
