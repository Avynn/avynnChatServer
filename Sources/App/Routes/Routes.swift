import Vapor

let room = Room()

extension Droplet {
    
    func setupRoutes() throws {
        get("hello") { req in
            var json = JSON()
            try json.set("hello", "world")
            return json
        }

        get("plaintext") { req in
            return "Hello, world!"
        }
        
        socket("chat") { req, ws in
            var userName: String? = nil
            var firstMessage: Bool = true
            
            try background{
                while(ws.state == .open){
                    try? ws.ping()
                    self.console.wait(seconds: 20)
                }
            }
            
            ws.onText = { ws, text in
                let json = try JSON(bytes: text.makeBytes())
                
                if (firstMessage == true){
                    if let u = json.object?["username"]?.string {
                        userName = u
                        room.connections[u] = ws
                        room.bot("\(u) has joined")
                    }
                    
                    if let u = userName, let m = json.object?["message"]?.string {
                        print("\(u): \(m)")
                        room.send(name: u, message: m)
                    }
                    
                    firstMessage = false
                } else {
                    if let u = json.object?["username"]?.string {
                        userName = u
                    }
                    
                    if let u = userName, let m = json.object?["message"]?.string {
                        print("\(u): \(m)")
                        room.send(name: u, message: m)
                    }
                }
            }
            
            ws.onClose = {ws, _, _, _ in
                guard let u = userName else {
                    return
                }
                
                print("\(u) has left")
                room.bot("\(u) has left")
                room.connections.removeValue(forKey: u)
            }
        }

        // response to requests to /info domain
        // with a description of the request
        get("info") { req in
            return req.description
        }

        get("description") { req in return req.description }
        
        try resource("posts", PostController.self)
    }
}
