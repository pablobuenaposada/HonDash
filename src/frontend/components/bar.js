class Bar {

    // @todo: refactor the constructor to pass an object
    // and not a list of arguments
    constructor(id, x, y, isVertical, backgroundColor, fillColor, minValue, maxValue, enableTextValue, textEnding, textFont, textWeight, textSize) {
        var element = document.getElementById(id);
        this.x = x;
        this.y = y;
        this.width = element.offsetWidth;
        this.height = element.offsetHeight;
        this.isVertical = isVertical;
        this.minValue = minValue;
        this.maxValue = maxValue;
        this.enableTextValue = enableTextValue;
        this.textEnding = textEnding;
        this.textFont = textFont;
        this.textWeight = textWeight;
        this.textSize = textSize;

        // Raphael paper object
        this.paper = Raphael(id, "100%", "100%");

        // Background
        this.background = this.paper.rect(x, y, this.width, this.height);
        this.background.attr({
            fill: backgroundColor,
            stroke: backgroundColor,
        });

        // Bar fill & stroke
        this.bar = this.paper.rect(x, y, this.width, this.height);
        this.bar.attr({
            fill: fillColor,
            stroke: fillColor,
        });

        // Center the text on the Bar
        this.text = this.paper.text(
            (this.width / 2) + x,
            y + (this.height / 2),
            ""
        );
    }

    refresh(value) {
        value = value > this.maxValue
            ? this.maxValue
            : (value < this.minValue)
            ? this.minValue
            : value;

        var verticalAttr = function () {
            return { width: this.width * value / this.maxValue }
        };

        var horizontalAttr = function () {
            var newHeight = this.height * value / this.maxValue;
            return {
                y: this.y - newHeight + this.height,
                height: newHeight
            }
        };

        this.bar.attr(this.isVertical
            ? verticalAttr()
            : horizontalAttr()
        );

        this.enableTextValue && this.text.attr({
            "font-family": this.textFont,
            "font-size": this.textSize
            "font-weight": this.textWeight,
            text: value + this.textEnding,
        });
    }
};
