#!/usr/bin/python3

"""
 contentApp class
 Simple web application for managing content

 Copyright Jesus M. Gonzalez-Barahona, Gregorio Robles 2009-2015
 jgb, grex @ gsyc.es
 TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
 October 2009 - March 2015
"""

import webapp
import csv


class contentApp (webapp.webApp):
    """Simple web application for managing content.

    Content is stored in a dictionary, which is intialized
    with the web content."""

    # Declare and initialize content
    content = {}
    content2 = {}

    def leer(self):
        try:
            with open("datos.csv") as csfile:
                entrada = csv.reader(csfile)
                for row in entrada:
                    valor1 = int(row[0])    # num
                    valor2 = row[1]         # url
                    self.content[valor1] = valor2
                    self.content2[valor2] = valor1
        except FileNotFoundError:
            print("No hay archivo")

    def write(self):
        with open("datos.csv", "w") as csvfile:
            escr = csv.writer(csvfile)
            for elem in self.content:
                escr.writerow([elem, self.content[elem]])

    def parse(self, request):
        """Return the resource name (including /)"""
        self.leer()  # Lee del fichero
        # devuelve nombre recurso (GET,..)
        # valor del recurso /bla
        # si es un post lo que haya en el body
        return (request.split(' ', 1)[0],
                request.split(' ', 2)[1],
                request.split('\r\n\r\n')[-1])

    def process(self, parsed):
        """Process the relevant elements of the request.

        Finds the HTML text corresponding to the resource name,
        ignoring requests for resources not in the dictionary.
        """
        method, resourceName, body = parsed

        if (resourceName == "/"):
            if (method == "GET"):
                httpCode = "200 OK"
                htmlBody = ("<html><body><form method= 'POST' action=''>" +
                            "<input type = 'text' name= 'url'>" +
                            "<input type= 'submit' value='Enviar'></form>" +
                            "<p>" + str(self.content) + "</p></html>")
            elif (method == "POST"):
                import urllib.parse
                url = urllib.parse.unquote(body)
                # comparar el content (LA URL)
                if ("=" in body):      # hay o no QS
                    url = url.split('=')[-1]
                    if url.startswith("http://") or url.startswith("https://"):
                        print("encuentro http://")
                    else:
                        url = "http://" + url

                    # COMPARAR PARA VER SI ESTA EN LA LISTA
                    if (url in self.content2):
                        httpCode = "404 Not Found"
                        htmlBody = ("<html><body>ya guardado en con url:" +
                                    "http://localhost:1234/" +
                                    str(self.content2[url]) + "</body></html>")
                    else:
                        self.content[len(self.content)] = url
                        self.content2[url] = len(self.content2)
                        self.write()
                        httpCode = "200 OK"
                        htmlBody = ("<html><body><p><a href = " +
                                    self.content[(len(self.content) - 1)] +
                                    ">" +
                                    self.content[(len(self.content) - 1)] +
                                    "</a></p><p><a href = " +
                                    self.content[(len(self.content) - 1)] +
                                    ">" + 'http://localhost:1234/' +
                                    str(len(self.content) - 1) +
                                    "</a></p></body></html>")
                else:
                    httpCode = "400 Bad Request"
                    htmlBody = ("<html><body>No hay cuerpo en el POST</html>")
            else:
                httpCode = "405 Method Not Allowed"
                htmlBody = ("<html><body>No se puede utilizar esa operacion" +
                            "</html>")

        else:   # Parte de los numeros
            resourceName = resourceName.split("/")[-1]
            if (resourceName == "favicon.ico"):
                httpCode = "404 Not Found"
                htmlBody = ("<html><body>Encontrado favicon</html>")
                recvSocket.close()
            elif (int(resourceName) in self.content):
                # redireccion
                resourceName = int(resourceName)
                httpCode = "301 Moved Permanently"
                htmlBody = ("<html><meta http-equiv= 'Refresh'" +
                            "content =5;url=" + self.content[resourceName] +
                            "><body><h1>Hola</h1></body></html>" +
                            "\r\n" +
                            "<html><body><p> Vas a ser redirigido en 5 seg" +
                            " a la pagina: " + self.content[resourceName] +
                            "</p></body></html>")
            else:
                httpCode = "404 Not Found"
                htmlBody = ("<html><body>Recurso no encontrado</html>")

        return (httpCode, htmlBody)

if __name__ == "__main__":
    testWebApp = contentApp("localhost", 1234)
