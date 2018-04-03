class Bar {

     constructor(id, x, y, isVertical, backgroundColor, fillColor, minValue, maxValue, enableTextValue, textEnding, textFont, textWeight, textSize){
        this.x = x;
        this.y = y;
        this.width = document.getElementById(id).offsetWidth;
        this.height = document.getElementById(id).offsetHeight;
        this.isVertical = isVertical;
        this.minValue = minValue;
        this.maxValue = maxValue;
        this.enableTextValue = enableTextValue;
        this.textEnding = textEnding;
        this.textFont = textFont;
        this.textWeight = textWeight;
        this.textSize = textSize;

        this.paper = Raphael(id, "100%", "100%");

        this.background = this.paper.rect(x, y, this.width, this.height);
        this.background.attr({fill: backgroundColor, stroke: backgroundColor});

        this.bar = this.paper.rect(x, y, this.width, this.height);
        this.bar.attr({fill: fillColor, stroke: fillColor});

        this.text = this.paper.text((this.width/2)+x, y+(this.height/2), "");
     }

    refresh(value){
        if (value > this.maxValue) {
            value = this.maxValue;
        }
        else if (value < this.minValue) {
            value = this.minValue;
        }

        if (this.isVertical) {
            this.newWidth = (this.width * value) / this.maxValue;
            this.bar.attr({width: this.newWidth});
        }
        else {
            this.newHeight = (this.height * value) / this.maxValue;
            this.bar.attr({y: (this.y - this.newHeight) + this.height  , height: this.newHeight});
        }

        if (this.enableTextValue) {
            this.text.attr({text: value+this.textEnding, "font-family": this.textFont, "font-weight": this.textWeight, "font-size": this.textSize});
        }
    }
};
