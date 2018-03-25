# Name: Ya Lien
# Class: CS496
from google.appengine.ext import ndb
import webapp2
import json

class Boat(ndb.Model):
    name = ndb.StringProperty(required=True)
    id = ndb.StringProperty()
    length = ndb.IntegerProperty()
    type = ndb.StringProperty()
    at_sea = ndb.BooleanProperty()
    
class BoatHandler(webapp2.RequestHandler):
    # Add a Boat
    def post(self): 
        boat_data = json.loads(self.request.body) #send in data
        new_boat = Boat(name=boat_data['name'],
                       type=boat_data['type'],
                       length=boat_data['length'])
        new_boat.at_sea = True # a new boat should start at sea
        new_boat.put()
        boat_dict = new_boat.to_dict()
        boat_dict['self'] = '/boat/' + new_boat.key.urlsafe()
        self.response.write(json.dumps(boat_dict))
        
    def get(self, id=None):
        #view a boat
        if id:
            the_boat = ndb.Key(urlsafe=id).get()
            if the_boat:
                the_boat_dict = the_boat.to_dict()
                the_boat_dict['self'] = '/boat/' + id
                self.response.write(json.dumps(the_boat_dict))
            else:
                self.response.status = 400
                self.response.write("Bad Request: Boat ID does not exist.")
        
        #list all of the boats if id not specified
        else: 
            boats = Boat.query().fetch()
            boat_list = {'b_list':[]}
            for b in boats: 
                id = b.key.urlsafe()
                boat_dict = b.to_dict()
                boat_dict['self'] = '/boat/' + id
                boat_dict['id'] = id
                boat_list['b_list'].append(boat_dict)          
            self.response.write(json.dumps(boat_list))
            
    # Remove a boat        
    def delete(self, id=None):
        if id:
            boat = ndb.Key(urlsafe=id).get()
            if boat: 
                for s in Slip.query(Slip.current_boat == id):
                    s.current_boat = ""
                    s.arrival_date = ""
                    slip.put()
                self.response.write('Slip Empty. ')
                
                boat.key.delete()
                self.response.write('Boat Deleted. ')
                
            else:
                self.response.status = 400
                self.response.write("Bad Request: Boat ID does not exist.") 
        else:
            self.response.status = 400
            self.response.write("Bad Request: Missing Boat ID.")
            
    # Modify a boat
    def patch(self, id=None):
        if id:
            boat = ndb.Key(urlsafe=id).get()
            if boat:
                boat_data = json.loads(self.request.body)
                if 'name' in boat_data:
                    boat.name = boat_data['name']
                if 'type' in boat_data:
                    boat.type = boat_data['type']
                if 'length' in boat_data:
                    boat.length = boat_data['length']
                if 'at_sea' in boat_data:
                    boat.at_sea = boat_data['at_sea']
                    if boat_data['at_sea'] == True:
                        for s in Slip.query(Slip.current_boat == id):
                            s.current_boat = ""
                            s.arrival_date = ""
                            s.put()
                        self.response.write('Boat Set to at_sea, Slip Empty')   
                boat.put()
                boat_dict = boat.to_dict()
                self.response.write(json.dumps(boat_dict))
            else:
                self.response.status = 400
                self.response.write("Bad Request: Boat ID does not exist.")
        else:
            self.response.status = 400
            self.response.write("Bad Request: Missing Boat ID.")
            
    # Replace a boat
    def put(self, id=None):
        if id:
            boat = ndb.Key(urlsafe=id).get()
            if boat:
                boat_data = json.loads(self.request.body)
                if 'name' in boat_data:
                    boat.name = boat_data['name']
                if 'type' in boat_data:
                    boat.type = boat_data['type']
                if 'length' in boat_data:
                    boat.length = boat_data['length']
                if 'at_sea' in boat_data:
                    boat.at_sea = boat_data['at_sea']
                    if boat_data['at_sea'] == True:
                        for s in Slip.query(Slip.current_boat == id):
                            s.current_boat = ""
                            s.arrival_date = ""
                            s.put()
                        self.response.write('Boat Set to at_sea, Slip Empty')    
                        
                boat.put()
                boat_dict = boat.to_dict()
                self.response.write(json.dumps(boat_dict))
                
            else:
                self.response.status = 400
                self.response.write("Bad Request: Boat ID does not exist.")
                
        else:
            self.response.status = 400
            self.response.write("Bad Request: Bad Request: Missing Boat ID.")
                      
                   
class Slip(ndb.Model):
    id = ndb.StringProperty()
    number = ndb.IntegerProperty(required=True)
    current_boat = ndb.StringProperty()
    arrival_date = ndb.StringProperty()
    
class SlipHandler(webapp2.RequestHandler):
    def post(self):
        slip_data = json.loads(self.request.body)
       
        if slip_data['number']:
            if Slip.query(Slip.number == slip_data['number']).get():
                self.response.status = 400
                self.response.write("Bad Request: Slip number in use.")
                
            else:   
                new_slip = Slip(number=slip_data['number'],
                                current_boat= "",
                                arrival_date= "")    
                new_slip.put()
        
                slip_dict = new_slip.to_dict()
                slip_dict['self'] = '/slip/' + new_slip.key.urlsafe()
                self.response.write(json.dumps(slip_dict))

    def get(self, id=None):
        if id:
            the_slip = ndb.Key(urlsafe=id).get()
            if the_slip:
                the_slip_dict = the_slip.to_dict()
                the_slip_dict['self'] = '/slip/' + id
                self.response.write(json.dumps(the_slip_dict))
            else:
                self.response.status = 400
                self.response.write("Bad Request: Slip ID does not exist.")
                   
        else: # if no id is provided list all slips
            slips = Slip.query().fetch()
            slip_list = {'s_list':[]}
            for s in slips: 
                id = s.key.urlsafe()
                slip_dict = s.to_dict()
                slip_dict['self'] = '/slip/' + id
                slip_dict['id'] = id
                slip_list['s_list'].append(slip_dict)          
            self.response.write(json.dumps(slip_list))
            
    # Remove a Slip
    def delete(self, id=None):
        if id:
            slip = ndb.Key(urlsafe=id).get()
            if slip:
                for b in Boat.query(Boat.id == slip.current_boat):
                    b.at_sea = True
                    b.put()
                self.response.write('Boat at this slip set to at_sea. ')
                
                slip.key.delete()
                self.response.write('Slip Deleted. ')
                
            else:
                self.response.status = 400
                self.response.write("Bad Request: Slip ID does not exist.") 
        else:
            self.response.status = 400
            self.response.write("Bad Request: Missing Slip ID.")       

    # Modify a Slip
    def patch(self, id=None):
        if id:
            slip = ndb.Key(urlsafe=id).get()
            if slip:
                slip_data = json.loads(self.request.body)
                if 'number' in slip_data:
                    if Slip.query(Slip.number == slip_data['number']).get():
                        self.response.status = 400
                        self.response.write("Bad Request: Slip number in use.")
                    else:
                        slip.number = slip_data['number']
                        
                if 'current_boat' in slip_data:
                    # check if the boat is currently parked at another slip
                    for s in Slip.query(Slip.current_boat == slip_data['current_boat']):
                        # remove the boat from another slip
                        s.current_boat = ""
                        s.arrival_date = ""
                    slip.current_boat = slip_data['current_boat']
                    
                if 'arrival_date' in slip_data:
                    slip.arrival_date = slip_data['arrival_date']
                    
                slip.put()
                slip_dict = slip.to_dict()
                self.response.write(json.dumps(slip_dict))
                
            else:
                self.response.status = 400
                self.response.write("Bad Request: Slip ID does not exist.")
        else:
            self.response.status = 400
            self.response.write("Bad Request: Missing Slip ID.")
    
    # Replace a Slip
    def put(self, id=None):
        if id:
            slip = ndb.Key(urlsafe=id).get()
            if slip:
                slip_data = json.loads(self.request.body)
                if 'number' in slip_data:
                    if Slip.query(Slip.number == slip_data['number']).get():
                        self.response.status = 400
                        self.response.write("Bad Request: Slip number in use.")
                    else:
                        slip.number = slip_data['number']
                        
                if 'current_boat' in slip_data:
                    # check if the boat is currently parked at another slip
                    for s in Slip.query(Slip.current_boat == slip_data['current_boat']):
                        # remove the boat from another slip
                        s.current_boat = ""
                        s.arrival_date = ""
                    slip.current_boat = slip_data['current_boat']
                    
                if 'arrival_date' in slip_data:
                    slip.arrival_date = slip_data['arrival_date']
                    
                slip.put()
                slip_dict = slip.to_dict()
                self.response.write(json.dumps(slip_dict))
                
            else:
                self.response.status = 400
                self.response.write("Bad Request: Slip ID does not exist.")
        else:
            self.response.status = 400
            self.response.write("Bad Request: Missing Slip ID.")

# [START main_page]
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write("hello")
# [END main_page]

# PATCH for Webapp2
allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/boat', BoatHandler),
    ('/boat/(.*)', BoatHandler),
    ('/slip', SlipHandler),
    ('/slip/(.*)', SlipHandler)   
], debug=True)
# [END app]