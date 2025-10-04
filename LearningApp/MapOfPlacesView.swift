//
//  MapOfPlacesView.swift
//  LearningApp
//
//  Created by Suprabhat kumar on 03/10/25.
//

import SwiftUI

struct MapOfPlacesView: View {
    var body: some View {
        VStack {
            MapView().frame(height: 300, alignment: .top)
            LocationImageView().frame(height: 300, alignment: .center).offset(y: -130).padding(.bottom, -130)
            VStack(alignment: .leading) {
                Text("India Gate").font(.title)
                HStack {
                    Text("New Delhi")
                    Spacer()
                    Text("India")
                }
            }.padding(.trailing, 30).padding(.leading, 10)
            Divider()
            Text("About India Gate").font(.title)
            Text("The India Gate, New Delhi, India is located at India country in the Monuments place category with the gps coordinates of 28° 36' 46.4184'' N and 77° 13' 46.0056 ...")
        }
        Spacer()
    }
}

#Preview {
    MapOfPlacesView()
}
