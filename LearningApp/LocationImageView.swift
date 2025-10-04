//
//  LocationImageView.swift
//  LearningApp
//
//  Created by Suprabhat kumar on 03/10/25.
//

import SwiftUI

struct LocationImageView: View {
    var body: some View {
        Image("IndiaGate").resizable().clipShape(Circle()).overlay {
            Circle().stroke(.white, lineWidth: 5)
                .shadow(radius: 7)
        }
    }
}

#Preview {
    LocationImageView()
}
