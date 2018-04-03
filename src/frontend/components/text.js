class Text {

     constructor(id, value, size, font, weight, style, prefix, suffix){
        this.id = id;
        this.prefix = prefix;
        this.suffix = suffix;

        document.getElementById(this.id).innerHTML = this.prefix+value+this.suffix;
        document.getElementById(this.id).style.fontSize = size+"px";
        document.getElementById(this.id).style.fontFamily = font;
        document.getElementById(this.id).style.fontWeight = weight;
        document.getElementById(this.id).style.fontStyle = style;
     }

     refresh(value){
        document.getElementById(this.id).innerHTML = this.prefix+value+this.suffix;
     }
 }