//
//  MapView.swift
//  LearningApp
//
//  Created by Suprabhat kumar on 03/10/25.
//

import SwiftUI
import MapKit

struct MapView: View {
    let locationCoordinate: CLLocationCoordinate2D
    var body: some View {
        Map(initialPosition: .region(region))
    }
    
    var region: MKCoordinateRegion {
        MKCoordinateRegion(center: locationCoordinate, span: MKCoordinateSpan(latitudeDelta: 0.1,longitudeDelta: 0.1))
    }
}

#Preview {
    MapView(locationCoordinate: landmarks[0].locationCoordinate)
}
