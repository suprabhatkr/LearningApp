//
//  ContentView.swift
//  LearningApp
//
//  Created by Suprabhat kumar on 02/10/25.
//

import SwiftUI

enum LearningViewType: Hashable {
    case basicLearningView
    case mapOfPlacesView
}

struct LearningView: Identifiable {
    let id = UUID()
    var title: String
    var viewType: LearningViewType
}

struct ContentView: View {
    var learningViews = [
        LearningView(title: "List", viewType: .basicLearningView),
        LearningView(title: "User Input", viewType: .basicLearningView),
        LearningView(title: "Buttons", viewType: .basicLearningView),
        LearningView(title: "Image with Map", viewType: .mapOfPlacesView)
    ]
    var body: some View {
        NavigationView {
            VStack {
                List(learningViews) {
                    learningView in NavigationLink(destination: {
                        switch learningView.viewType {
                        case .basicLearningView:
                            BasicLearningView()
                        case .mapOfPlacesView:
                            LandmarkListView()
                        }
                    }) {
                        Text(learningView.title)
                    }
                }
            }
        }
    }
}

#Preview {
    ContentView()
}
