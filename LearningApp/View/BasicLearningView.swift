//
//  BasicLearningView.swift
//  LearningApp
//
//  Created by Suprabhat kumar on 03/10/25.
//

import SwiftUI

struct BasicLearningView: View {
    @State var counter = 0
    @State var name = ""
    @State var email = ""
    var songs = [
        Song(title: "Photograph", artist: "Ed Sheeren"),
        Song(title: "Baby", artist: "Just Beiber"),
        Song(title: "Despacito", artist: "Louis Fonci"),
        Song(title: "Hips Don't lie", artist: "Shakira")
    ]
    var body: some View {
        VStack(spacing: 20) {
            Text("You have tapped on the button \(counter) times")
            Button("Tap Me") {
                self.counter += 1
            }
            Button("Reset") {
                self.counter = 0
            }
        }
        .padding()
        NavigationView {
            List(songs) {
                song in VStack {
                    NavigationLink(destination: SongDetailView(song: song)) {
                        Text(song.title).font(.title)
                    }
                }
            }
        }
        VStack(spacing: 20) {
            TextField("Enter your Name : ", text: $name).border(.blue)
            TextField("Enter your Email : ", text: $email).border(.blue)
            Text("The email address of \(name) is \(email)")
        }
    }
}

#Preview {
    BasicLearningView()
}
