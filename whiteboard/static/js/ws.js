var socket = null
var uid=null
var isopen = false
var callback=null

function getRequest(url,responseType) {
   const promise = new Promise((resolve, reject) => {
       const Http = new XMLHttpRequest()
       Http.open('GET', url)
       Http.responseType = responseType

       Http.onload = () => {
           resolve(Http.response)
       }

       Http.send()
   })
   return promise
}

window.onload = function() {

   socket = new WebSocket("ws://"+window.location.host+"/ws")

   socket.onopen = function() {
      console.log("Connected!")
      isopen = true
      socket.send('{"name":"whiteboard"}')
      let path=window.location.href
      let pos=path.indexOf("?")
      if (pos>0) {
         let boardId=path.substring(pos+1)
         console.log("Loading board ID:"+boardId)
         getRequest("/openboard/"+boardId,"json")
            .then(shapeList => { 
                  shapeList.forEach(
                     shape => callback.shape(shape)  
                  )
                  let url=window.location.protocol+"//"+window.location.host+"/views/whiteboard.html?"+boardId
                  document.getElementById("board_link").value=url
                  socket.send(JSON.stringify({"uid":uid,"boardid":boardId,"action":"openboard"}))
                  }
               ) 
         }
      else {
         console.log("New board")
         getRequest("/newboard","json")
            .then(resp => {
                  let boardId=resp["boardId"]
                  let url=window.location.protocol+"//"+window.location.host+"/views/whiteboard.html?"+boardId
                  window.location.href=url
                  }
               ) 
         }
      }

   socket.onmessage = function(e) {
      if (typeof e.data == "string") {
         console.log("Action received: " + e.data)
         msg=JSON.parse(e.data)
         if("setuid" in msg) {
            uid=msg["setuid"]
         }
         else
            if(callback) {
               if (msg["action"]=="move") {
                  callback.move(msg["uid"],msg["x"],msg["y"],msg["color"])
               }
               else if (msg["action"]=="keypressed") {
                  callback.keypressed(msg["uid"],msg["key"],msg["x"],msg["y"],msg["textmode"],msg["color"])
               }
               else if (msg.hasOwnProperty("shape")) {
                  callback.clean(msg["uid"])
                  callback.shape(msg)
                  }
            }
      }
   }

   socket.onclose = function(e) {
      console.log("Connection closed.")
      socket = null
      isopen = false
   }

}

function sendPosition(uid,x,y,action,shape,color) {
   if (isopen) {
      socket.send(JSON.stringify({"uid":uid,"x":x,"y":y,"action":action,"shape":shape,"color":color}))
      console.log("Position sent.")
   } else {
      console.log("Connection not opened.")
   }
}

function sendKeyPressed(uid,key,x,y,textmode,color) {
   if (isopen) {
      socket.send(JSON.stringify({"uid":uid,"x":x,"y":y,"action":"keypressed","key":key,"textmode":textmode,"color":color}))
      console.log("Key sent.")
   } else {
      console.log("Connection not opened.")
   }
}

function sendUndo(uid) {
   if (isopen) {
      socket.send(JSON.stringify({"uid":uid,"action":"undo"}))
      console.log("Undo sent.")
   } else {
      console.log("Connection not opened.")
   }
}

