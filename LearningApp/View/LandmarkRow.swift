//
//  LandmarkRow.swift
//  LearningApp
//
//  Created by Suprabhat kumar on 04/10/25.
//

import SwiftUI

struct LandmarkRow: View {
    var landmark: Landmark
    @Environment(ModelData.self) var modelData
    var landMarkIndex: Int {
        modelData.landmarks.firstIndex(where: {$0.id == landmark.id})!
    }
    
    var body: some View {
        @Bindable var modelData = modelData
        HStack {
            NavigationLink(destination: MapOfPlacesView(landmark: landmark)) {
                HStack {
                    landmark.image.resizable().frame(width: 50, height: 50, alignment: .leading)
                    Text(landmark.name).foregroundColor(.black)
                }
            }
            Spacer()
            FavoriteView(isSet: $modelData.landmarks[landMarkIndex].isFavorite)
        }
    }
}

#Preview {
    LandmarkRow(landmark: ModelData().landmarks[0])
}
