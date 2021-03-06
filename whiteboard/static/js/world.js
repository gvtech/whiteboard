
class World {
   constructor (board) {
      this.canvas = board
      this.context = this.canvas.getContext('2d')
      this.localsnake= new Drawing(this.context,'#00AA00')
      this.remotedraw=[]
      this.mousedown=false
      this.trainingMode = false
      this.curshape= "?"
      this.lastx=0
      this.lasty=0
      this.textmode="normal"
   }

   move(uid,x,y) {
      if(!(uid in this.remotedraw)) {
         this.remotedraw[uid]=new Drawing(this.context,'#AA0000')
      }
      this.remotedraw[uid].move(x,y)
   }

   keypressed(uid,key,x,y,textmode) {
      if(!(uid in this.remotedraw)) {
         this.remotedraw[uid]=new Drawing(this.context,'#AA0000')
      }
      this.remotedraw[uid].keypressed(key,x,y,textmode)
   }

   clear() {
      this.context.clearRect(0, 0, this.canvas.width, this.canvas.height)
   }

   clean(uid) {
      if (this.trainingMode)
         this.clear()
      else
         this.localsnake.clean()
      if(uid in this.remotedraw)
            this.remotedraw[uid].clean()
   }

   shape(msg) {
      if(!(msg.uid in this.remotedraw)) {
         this.remotedraw[msg.uid]=new Drawing(this.context,'#AA0000')
      }
      this.remotedraw[msg.uid].shape(msg)
   }

   changeTextMode(key) {
      if (key=="ArrowUp") {
         if (this.textmode=="normal")
            this.textmode="exponent"
         else if (this.textmode=="indice")
            this.textmode="normal"
         }
      else if (key=="ArrowDown") {
         if (this.textmode=="exponent")
            this.textmode="normal"
         else if (this.textmode=="normal")
            this.textmode="indice"

      }
   }
}