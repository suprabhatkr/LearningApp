//
//  MapView.swift
//  LearningApp
//
//  Created by Suprabhat kumar on 03/10/25.
//

import SwiftUI
import MapKit

struct MapView: View {
    var body: some View {
        Map(initialPosition: .region(region))
    }
    
    var region: MKCoordinateRegion {
        MKCoordinateRegion(center: CLLocationCoordinate2D(latitude: 28.6129,longitude: 77.2295), span: MKCoordinateSpan(latitudeDelta: 0.1,longitudeDelta: 0.1))
    }
}

#Preview {
    MapView()
}
