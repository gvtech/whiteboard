
class Drawing{ 
   constructor(context,color) {
      this.color = color
      this.snake = []
      this.context=context
      }

   draw(x,y,color) {
      if (this.snake.length>0) {
         this.context.beginPath()
         this.context.strokeStyle = color
         this.context.lineWidth = 1
         let coord=this.snake[this.snake.length-1]
         this.context.moveTo(coord[0],coord[1])   
         this.context.lineTo(x,y)
         this.context.stroke()
         }
 	}

   move(x,y) {
      this.draw(x,y,this.color)
      this.snake.push([x,y])
      }

   keypressed(key,x,y,textmode) {
      this.snake=[]
      this.context.lineWidth = 1
      let shift=0
      if (textmode=="normal") {
         this.context.font = '24px Arial'
         }
      else {
         this.context.font = '12px Arial'
         if (textmode=="exponent") {
            shift=-18
            }
         else if (textmode=="indice") {
            shift=12
            }
         }
      this.context.fillText(key, x, y+shift)
      return this.context.measureText(key).width
   }

   clean() {
      if (this.snake.length>0) {
         this.context.beginPath()
         this.context.strokeStyle = '#ffffff'
         this.context.lineWidth = 2
         let coord=this.snake.shift()
         this.context.moveTo(coord[0],coord[1])   
         while(this.snake.length > 0) {
            coord=this.snake.shift()
            this.context.lineTo(coord[0],coord[1])
            }
         this.context.stroke()
         }
      }

   shape(s) {
      this.context.beginPath()
      this.context.strokeStyle = this.color
      this.context.lineWidth = 3
      if (s.shape=="rectangle") {
         this.context.strokeRect(s.x, s.y, s.dx, s.dy) 
         }
      else if (s.shape=="elipse") {
         this.context.ellipse(s.x+s.dx/2, s.y+s.dy/2, s.dx/2,s.dy/2,0, 0, 2 * Math.PI)
         }
      else if (s.shape=="triangle") {
         this.context.moveTo(s.x+s.dx/2, s.y)
         this.context.lineTo(s.x+s.dx, s.y+s.dy)
         this.context.lineTo(s.x, s.y+s.dy)
         this.context.lineTo(s.x+s.dx/2, s.y)
         }
      else if (s.shape=="hline") {
         this.context.moveTo(s.x, s.y)
         this.context.lineTo(s.x+s.dx, s.y)
         }
      else if (s.shape=="vline") {
         this.context.moveTo(s.x, s.y)
         this.context.lineTo(s.x, s.y+s.dy)
         }
      else if (s.shape=="sigma") {
         this.context.moveTo(s.x+s.dx, s.y)
         this.context.lineTo(s.x, s.y)
         this.context.lineTo(s.x+s.dx/2, s.y+s.dy/2)
         this.context.lineTo(s.x, s.y+s.dy)
         this.context.lineTo(s.x+s.dx, s.y+s.dy)
         }
      else if (s.shape=="leftbracket") {
         this.context.moveTo(s.x+s.dx, s.y)
         this.context.lineTo(s.x, s.y)
         this.context.lineTo(s.x,s.y+s.dy)
         this.context.lineTo(s.x+s.dx, s.y+s.dy)
         }
      else if (s.shape=="rightbracket") {
         this.context.moveTo(s.x,s.y)
         this.context.lineTo(s.x+s.dx, s.y)
         this.context.lineTo(s.x+s.dx, s.y+s.dy)
         this.context.lineTo(s.x,s.y+s.dy)
         }
      else if (s.shape=="integral") {
         this.context.moveTo(s.x+s.dx,s.y)
         this.context.bezierCurveTo(s.x+s.dx*0.6,s.y+s.dy*0.1,s.x+s.dx*0.4,s.y+s.dy*0.9,s.x,s.y+s.dy)
         }
      else if (s.shape=="uparrow") {
         this.context.moveTo(s.x,s.y+s.dy)
         this.context.lineTo(s.x+s.dx/2, s.y)
         this.context.lineTo(s.x+s.dx, s.y+s.dy)
         }
      else if (s.shape=="downarrow") {
         this.context.moveTo(s.x,s.y)
         this.context.lineTo(s.x+s.dx/2, s.y+s.dy)
         this.context.lineTo(s.x+s.dx, s.y)
         }
      else if (s.shape=="leftarrow") {
         this.context.moveTo(s.x+s.dx,s.y)
         this.context.lineTo(s.x, s.y+s.dy/2)
         this.context.lineTo(s.x+s.dx,s.y+s.dy)
         }
      else if (s.shape=="rightarrow") {
         this.context.moveTo(s.x,s.y)
         this.context.lineTo(s.x+s.dx, s.y+s.dy/2)
         this.context.lineTo(s.x,s.y+s.dy)
         }
      this.context.stroke()
   }
}
