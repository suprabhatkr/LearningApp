//
//  LandmarkListView.swift
//  LearningApp
//
//  Created by Suprabhat kumar on 04/10/25.
//

import SwiftUI

struct LandmarkListView: View {
    var body: some View {
        NavigationSplitView {
            List(landmarks) {
                landmark in LandmarkRow(landmark: landmark)
            }
        } detail: {
            Text("Select a landmark")
        }
    }
}

#Preview {
    LandmarkListView()
}
