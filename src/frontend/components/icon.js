class Icon {

    constructor(id, path_off, path_on){
        this.id = id;
        this.path_off = path_off;
        this.path_on = path_on;
        var img = document.createElement("img");
        img.src = "icons/"+this.path_off;
        img.style.width = "100%";
        document.getElementById(this.id).appendChild(img);
    }

    refresh(value){
        if(value > 0){
            var img = document.createElement("img");
            img.src = "icons/"+this.path_on;
            img.style.width = "100%";
        }
        else{
            var img = document.createElement("img");
            img.src = "icons/"+this.path_off;
            img.style.width = "100%";
        }
        document.getElementById(this.id).innerHTML = '';
        document.getElementById(this.id).appendChild(img);
    }
}