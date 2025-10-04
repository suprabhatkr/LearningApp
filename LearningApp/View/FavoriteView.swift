//
//  FavoriteView.swift
//  LearningApp
//
//  Created by Suprabhat kumar on 04/10/25.
//

import SwiftUI

struct FavoriteView: View {
    @Binding var isSet: Bool
    var body: some View {
        Button {
            isSet.toggle()
        } label: {
            Label("Toggle Favorites", systemImage: isSet ? "star.fill" : "star").labelStyle(.iconOnly).foregroundColor(isSet ? .yellow : .gray)
        }
    }
}

#Preview {
    FavoriteView(isSet: .constant(true))
}
