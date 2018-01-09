//
//  webSocketJson.swift
//  chatServerPackageDescription
//
//  Created by Avynn Donaghe on 1/5/18.
//

import Vapor

extension WebSocket {
    func send(_ json: JSON) throws {
        let js = try json.makeBytes()
        try send(js.makeString())
    }
}
