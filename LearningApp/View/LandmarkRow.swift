//
//  LandmarkRow.swift
//  LearningApp
//
//  Created by Suprabhat kumar on 04/10/25.
//

import SwiftUI

struct LandmarkRow: View {
    var landmark: Landmark
    var body: some View {
        NavigationLink(destination: MapOfPlacesView(landmark: landmark)) {
            HStack {
                landmark.image.resizable().frame(width: 50, height: 50, alignment: .leading)
                Text(landmark.name).foregroundColor(.black)
                Spacer()
            }
        }
    }
}

#Preview {
    LandmarkRow(landmark: landmarks[1])
}
