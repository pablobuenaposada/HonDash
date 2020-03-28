class Gauge {

    constructor(args) {
        var gaugeDefaults = {
            min: 0,
            max: 100,
            value: 0,
            decimals: 0,
            gaugeWidthScale: 1,
            valueMinFontSize: 60,
            labelMinFontSize: 20,
            startAnimationTime: 0,
            refreshAnimationTime: 0,
            gaugeColor: "#edebeb",
            labelFontColor: "black",
            label: "GAUGE",
        };

        this.gauge = new JustGage(Object.assign({}, gaugeDefaults, args));
    }

    refresh(value){
        this.gauge.refresh(value);
    }

    setSectors(sectors){
        this.gauge.config.customSectors = {length: true, ranges: sectors};
    }

    setLabel(label){
        this.gauge.config.label = label;
        this.gauge.txtLabel.attr({"text": this.gauge.config.label});
    }

    setMax(max){
        this.gauge.refresh(null, max);
    }

    setDecimals(decimals){
        this.gauge.config.decimals = decimals;
    }

    setTextColor(newColor){
        this.gauge.config.labelFontColor = newColor;
        this.gauge.txtValue.attr({"fill": this.gauge.config.labelFontColor});

        this.gauge.config.valueFontColor = newColor;
        this.gauge.txtLabel.attr({"fill": this.gauge.config.valueFontColor});

        this.gauge.txtMin.attr({"fill": this.gauge.config.labelFontColor});

        this.gauge.txtMax.attr({"fill": this.gauge.config.labelFontColor});
    }

    setBackgroundColor(color){
        this.gauge.config.gaugeColor = color;
        this.gauge.gauge.attr({"fill": this.gauge.config.gaugeColor});
    }
}