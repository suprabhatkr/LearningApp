//
//  Landmark.swift
//  LearningApp
//
//  Created by Suprabhat kumar on 04/10/25.
//

import MapKit
import SwiftUI

struct Landmark: Codable, Hashable, Identifiable {
    var id: Int16
    var isFeatured: Bool
    var isFavorite: Bool
    var name: String
    var category: String
    var city: String
    var state: String
    var description: String
    var park: String
    
    private var coordinates: Coordinate
    
    struct Coordinate: Hashable, Codable {
        var longitude: Double
        var latitude: Double
    }
    
    var locationCoordinate: CLLocationCoordinate2D {
        CLLocationCoordinate2D(
            latitude: coordinates.latitude,
            longitude: coordinates.longitude
        )
    }
    
    private var imageName: String
    
    var image: Image {
        Image(imageName)
    }
}
