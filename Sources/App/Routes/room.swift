//
//  room.swift
//  chatServerPackageDescription
//
//  Created by Avynn Donaghe on 1/5/18.
//

import Vapor

class Room{
    var connections: [String: WebSocket]
    
    func bot(_ message: String){
        send(name: "Bot", message: message)
    }
    
    func send(name: String, message: String){
        let messageNode: [String: NodeRepresentable] = [
            "username": name,
            "message": message
        ]
        
        guard let json = try? JSON(node: messageNode) else {
            return
        }
        
        guard let js = try? json.makeBytes() else {
            return
        }
        
        for (userName, socket) in connections {
            try? socket.send(js.makeString())
        }
    }
    
    init (){
        connections = [:]
    }
}
