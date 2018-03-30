class Text {

     constructor(id, value, size, font, weight, prefix, suffix){
        this.id = id;
        this.prefix = prefix;
        this.suffix = suffix;

        document.getElementById(this.id).innerHTML = this.prefix+value+this.suffix;
        document.getElementById(this.id).style.fontSize = size+"px";
        document.getElementById(this.id).style.fontFamily = font;
        document.getElementById(this.id).style.fontWeight = weight;
     }

     refresh(value){
        document.getElementById(this.id).innerHTML = this.prefix+value+this.suffix;
     }
 }