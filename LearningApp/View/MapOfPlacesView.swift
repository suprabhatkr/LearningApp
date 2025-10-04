//
//  MapOfPlacesView.swift
//  LearningApp
//
//  Created by Suprabhat kumar on 03/10/25.
//

import SwiftUI

struct MapOfPlacesView: View {
    let landmark: Landmark
    var body: some View {
        VStack {
            MapView(locationCoordinate: landmark.locationCoordinate).frame(height: 300, alignment: .top)
            LocationImageView(locationImage: landmark.image).frame(height: 300, alignment: .center).offset(y: -130).padding(.bottom, -130)
            VStack(alignment: .leading) {
                Text(landmark.name).font(.title)
                HStack {
                    Text(landmark.city)
                    Spacer()
                    Text(landmark.state)
                }
            }.padding(.trailing, 30).padding(.leading, 10)
            Divider()
            Text("About \(landmark.name)").font(.title)
            Text(landmark.description)
        }
        Spacer()
    }
}

#Preview {
    MapOfPlacesView(landmark: landmarks[0])
}
