#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Reservation:
    def __init__(self, id=0, idRestaurant=0, name="", email="", dateTime="", status=""):
        self.id = id
        self.idRestaurant = idRestaurant
        self.name = name
        self.email = email
        self.dateTime = dateTime
        self.status = status