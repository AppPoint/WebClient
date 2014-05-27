class Restaurant:
    def __init__(self, idRestaurant=0, name="", adress="", latitude=0, longitude=0, placesID="", email="", password="", description="", referencePlaces="", isPoint=False):
        self.idRestaurant = idRestaurant
        self.name = name
        self.adress = adress
        self.latitude = latitude
        self.longitude = longitude
        self.placesID = placesID
        self.email = email
        self.password = password
        self.description = description
        self.referencePlaces = referencePlaces
        self.isPoint = isPoint