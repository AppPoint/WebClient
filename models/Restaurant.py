#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Restaurant:
    def __init__(self, idRestaurant=0, name="", adress="", latitude=0, longitude=0, placesID="", email="", password="", description="", referencePlaces="", isPoint=False, featureReservation=False, featureMenu=False):
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
        self.featureReservation = featureReservation
        self.featureMenu = featureMenu


    def to_json(self):
        return {"name": self.name,
                "adress": self.adress,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "placesID": self.placesID,
                "email": self.email,
                "password": self.password,
                "description": self.description,
                "referencePlaces": self.referencePlaces,
                "isPoint": self.isPoint,
                "featureReservation": self.featureReservation,
                "featureMenu": self.featureMenu
                }