class Text {

     constructor(id, value, size, font, weight, style, prefix, suffix){
        this.element = document.getElementById(id);
        this.prefix = prefix;
        this.suffix = suffix;

        this.element.innerHTML = this.prefix+value+this.suffix;
        this.element.style.fontSize = size+"vw";
        this.element.style.fontFamily = font;
        this.element.style.fontWeight = weight;
        this.element.style.fontStyle = style;
     }

     refresh(value){
        this.element.innerHTML = this.prefix+value+this.suffix;
     }
 }