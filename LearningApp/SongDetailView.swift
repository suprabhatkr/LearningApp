//
//  SongDetailView.swift
//  LearningApp
//
//  Created by Suprabhat kumar on 03/10/25.
//

import SwiftUI

struct Song: Identifiable {
    var id = UUID()
    var title: String
    var artist: String
}

struct SongDetailView: View {
    var song: Song
    var body: some View {
        VStack {
            Text(song.title)
            Text(song.artist)
        }
    }
}

#Preview {
    SongDetailView(song: Song(title: "Senorita", artist: "Adele"))
}
