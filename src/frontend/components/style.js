class Style{

    constructor(args){
        this.dayBackgroundColor = "white";
        this.dayTextColor = "black";
        this.dayBackgroundGaugeColor = "#edebeb";
        this.nightBackgroundColor = "black";
        this.nightTextColor = "white";
        this.nightBackgroundGaugeColor = "#edebeb";
        this.currentStyle = null;
    }

    refresh(value){
        if (this.currentStyle == value){ return; }
        if (value == "night"){
            this.currentStyle = value;
            document.body.style.backgroundColor = this.nightBackgroundColor;
            for (var name in window) {
                try{
                  if (window[name].constructor.name == 'Text'){
                    window[name].setColor(this.nightTextColor);
                  }
                  else if (window[name].constructor.name == 'Gauge'){
                    window[name].setTextColor(this.nightTextColor);
                    window[name].setBackgroundColor(this.nightBackgroundGaugeColor);
                  }
                  else if (window[name].constructor.name == 'Bar'){
                    window[name].setBackgroundColor(this.nightBackgroundGaugeColor);
                  }
                }catch(error){
                }
            }
        }
        else if (value == "day"){
            this.currentStyle = value;
            document.body.style.backgroundColor = this.dayBackgroundColor;
            for (var name in window) {
                try{
                  if (window[name].constructor.name == 'Text'){
                    window[name].setColor(this.dayTextColor);
                  }
                  else if (window[name].constructor.name == 'Gauge'){
                    window[name].setTextColor(this.dayTextColor);
                    window[name].setBackgroundColor(this.dayBackgroundGaugeColor);
                  }
                  else if (window[name].constructor.name == 'Bar'){
                    window[name].setBackgroundColor(this.dayBackgroundGaugeColor);
                  }
                }catch(error){
                }
            }
        }
    }

    setDayBackgroundColor(color){
        this.dayBackgroundColor = color;
    }

    setNightBackgroundColor(color){
        this.nightBackgroundColor = color;
    }

    setDayTextColor(color){
        this.dayTextColor = color;
    }

    setNightTextColor(color){
        this.nightTextColor = color;
    }

    setDayBackgroundGaugeColor(color){
        this.dayBackgroundGaugeColor = color;
    }

    setNightBackgroundGaugeColor(color){
        this.nightBackgroundGaugeColor = color;
    }
}