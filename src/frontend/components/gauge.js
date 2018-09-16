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
        this.gauge.refresh(null, null, label);
    }

    setMax(max){
        this.gauge.refresh(null, max);
    }

    setDecimals(decimals){
        this.gauge.config.decimals = decimals;
    }
}