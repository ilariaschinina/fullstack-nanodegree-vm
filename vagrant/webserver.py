#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote, parse_qs
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from database_setup import Restaurant, Base, MenuItem

#Create session and connect to DB 
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                output = ""
                #Create a link to create a new restaurant
                output += "<a href = '/restaurants/new' > Make a New Restaurant Here </a></br></br>"
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output += "<html><body>"
                for restaurant in restaurants:
                    output += restaurant.name
                    restaurant_id = restaurant.id
                    output += "<br />"
                    #Add Edit and Delete Links
                    output += "<a href = '/restaurants/%s/edit'>Edit</a>" % restaurant_id
                    output += "<br />"
                    output += "<a href = '/restaurants/%s/delete'> Delete</a>" % restaurant_id
                    output += "<br />""<br />""<br />"
                    
                output += "</body></html>"
                self.wfile.write(output.encode())
                print(output.encode())
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method = 'POST' action = '/restaurants/new'>"
                output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output.encode())
                return

            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if myRestaurantQuery !=[]:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += myRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method = 'POST' action = '/restaurants/%s/edit'>" % restaurantIDPath 
                    output += "<input name = 'newRestaurantName' type = 'text' placeholder = '%s' >" % myRestaurantQuery.name
                    output += "<input type='submit' value='Rename'>"
                    output += "</form></body></html>"
                    self.wfile.write(output.encode())
                    return
            
            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if myRestaurantQuery !=[]:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1> Are you sure you want to delete %s?" % myRestaurantQuery.name
                    output += "<form method = 'POST' action = '/restaurants/%s/delete'>" % restaurantIDPath
                    output += "<input type='submit' value='Delete'>"
                    output += "</form></body></html>"
                    self.wfile.write(output.encode())
                    return

            # if self.path.endswith("/hello"):
            #     self.send_response(200)
            #     self.send_header('Content-type', 'text/html')
            #     self.end_headers()
            #     output = ""
            #     output += "<html><body>"
            #     output += "<h1>Hello!</h1>"
            #     output += '''<form method='POST' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"></form>'''
            #     output += "</body></html>"
            #     self.wfile.write(output.encode())
            #     print(output.encode())
            #     return
            # if self.path.endswith("/hola"):
            #     self.send_response(200)
            #     self.send_header('Content-type', 'text/html')
            #     self.end_headers()
            #     output = ""
            #     output += "<html><body>"
            #     output += "<h1> &#161 Hola! </h1><a href = '/hello' >Back to Hello</a>"
            #     output += '''<form method='POST' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            #     output += "</body></html>"
            #     self.wfile.write(output.encode())
            #     print(output.encode())
            #     return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)
    
    
    def do_POST(self):
        try:    
            if self.path.endswith("/restaurants/new"):
                length = int(self.headers.get('Content-length', 0))
                body = self.rfile.read(length).decode()
                fields = parse_qs(body)
                messagecontent = fields['newRestaurantName'][0]
                newRestaurant = Restaurant(name=messagecontent)
                session.add(newRestaurant)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
        except:
            pass

        try:    
            if self.path.endswith("/edit"):
                length = int(self.headers.get('Content-length', 0))
                body = self.rfile.read(length).decode()
                fields = parse_qs(body)
                messagecontent = fields['newRestaurantName'][0]
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if myRestaurantQuery != []:
                    myRestaurantQuery.name = messagecontent
                    session.add(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
        except:
            pass

        try:    
            if self.path.endswith("/delete"):
                length = int(self.headers.get('Content-length', 0))
                body = self.rfile.read(length).decode()
                fields = parse_qs(body)
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if myRestaurantQuery != []:
                    session.delete(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
        except:
            pass

        # try:
        #     self.send_response(301)
        #     self.send_header('Content-type', 'text/html')
        #     self.end_headers()
        #     length = int(self.headers.get('Content-length', 0))
        #     body = self.rfile.read(length).decode()
        #     params = parse_qs(body)
        #     messagecontent = params['message'][0]
        #     output = ""
        #     output += "<html><body>"
        #     output += " <h2> Okay, how about this: </h2>"
        #     output += "<h1> %s </h1>" % messagecontent
        #     output += '''<form method='POST' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
        #     output += "</body></html>"
        #     self.wfile.write(output.encode())
        #     print(output.encode())
        # except:
        #     pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print(" ^C entered, stopping web server...")
        server.socket.close()

if __name__ == '__main__':
    main()