//
//  LandmarkListView.swift
//  LearningApp
//
//  Created by Suprabhat kumar on 04/10/25.
//

import SwiftUI

struct LandmarkListView: View {
    @Environment(ModelData.self) var modelData
    @State var isFavorite = false
    
    var favoriteLandmarks: [Landmark] {
        modelData.landmarks.filter {
            landmark in (!isFavorite || landmark.isFavorite)
        }
    }
    
    var body: some View {
        NavigationSplitView {
            List {
                Toggle("Show Favorites only", isOn: $isFavorite)
                ForEach(favoriteLandmarks) {
                    landmark in LandmarkRow(landmark: landmark)
                }
            }.animation(.default, value: favoriteLandmarks)
        } detail: {
            Text("Select a landmark")
        }
    }
}

#Preview {
    LandmarkListView()
}
