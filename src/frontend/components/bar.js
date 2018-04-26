class Bar {

    constructor(args) {
        var element = document.getElementById(args.id);
        this.x = args.x || 0;
        this.y = args.y || 0;
        this.width = element.offsetWidth;
        this.height = element.offsetHeight;
        this.isVertical = args.isVertical || false;
        this.minValue = args.minValue || 0;
        this.maxValue = args.maxValue || 100;
        this.enableTextValue = args.enableTextValue !== undefined
            ? args.enableTextValue : true;
        this.textEnding = args.textEnding !== undefined
            ? args.textEnding : "%";
        this.textFont = args.textFont || "Arial";
        this.textWeight = args.textWeight || "bold";
        this.textSize = args.textSize || 20;
        var backgroundColor = args.backgroundColor || "#edebeb";

        // Raphael paper object
        this.paper = Raphael(id, "100%", "100%");

        // Background
        this.background = this.paper.rect(this.x, this.y, this.width, this.height);
        this.background.attr({
            fill: backgroundColor,
            stroke: backgroundColor,
        });

        // Bar fill & stroke
        this.bar = this.paper.rect(this.x, this.y, this.width, this.height);
        this.bar.attr({
            fill: args.fillColor,
            stroke: args.fillColor,
        });

        // Center the text on the Bar
        this.text = this.paper.text(
            (this.width / 2) + this.x,
            this.y + (this.height / 2),
            ""
        );
    }

    refresh(value) {
        value = value > this.maxValue
            ? this.maxValue
            : (value < this.minValue)
            ? this.minValue
            : value;

        if (this.isVertical) {
            this.newWidth = (this.width * value) / this.maxValue;
            this.bar.attr({width: this.newWidth});
        }
        else {
            this.newHeight = (this.height * value) / this.maxValue;
            this.bar.attr({y: (this.y - this.newHeight) + this.height  , height: this.newHeight});
        }

        this.enableTextValue && this.text.attr({
            "font-family": this.textFont,
            "font-size": this.textSize,
            "font-weight": this.textWeight,
            text: value + this.textEnding,
        });
    }
};
