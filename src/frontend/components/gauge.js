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
        // patching justgage library to add dynamic labeling
        this.gauge.refresh(null, null, label);
        this.gauge.config.label = label;
        this.gauge.txtLabel.attr({"text": this.gauge.config.label});
        setDy(this.gauge.txtLabel, this.gauge.params.labelFontSize, this.gauge.params.labelY);
    }

    setMax(max){
        this.gauge.refresh(null, max);
    }

    setDecimals(decimals){
        this.gauge.config.decimals = decimals;
    }

    setTextColor(newColor){
        // patching justgage library to add dynamic label coloring
        this.gauge.config.labelFontColor = newColor;
        this.gauge.txtValue.attr({"fill": this.gauge.config.labelFontColor});
        setDy(this.gauge.txtValue, this.gauge.params.labelFontSize, this.gauge.params.labelY);

        // patching justgage library to add dynamic value coloring
        this.gauge.config.valueFontColor = newColor;
        this.gauge.txtLabel.attr({"fill": this.gauge.config.valueFontColor});
        setDy(this.gauge.txtValue, this.gauge.params.valueFontSize, this.gauge.params.valueY);

        // patching justgage library to add dynamic min value coloring
        this.gauge.txtMin.attr({"fill": this.gauge.config.labelFontColor});
        setDy(this.gauge.txtMin, this.gauge.params.minFontSize, this.gauge.params.minY);

        // patching justgage library to add dynamic max value coloring
        this.gauge.txtMax.attr({"fill": this.gauge.config.labelFontColor});
        setDy(this.gauge.txtMax, this.gauge.params.minFontSize, this.gauge.params.minY);
    }

    setBackgroundColor(color){
        // patching justgage library to add dynamic background coloring
        this.gauge.config.gaugeColor = color;
        this.gauge.gauge.attr({"fill": this.gauge.config.gaugeColor});
        setDy(this.gauge.gauge, this.gauge.params.minFontSize, this.gauge.params.minY);
    }
}