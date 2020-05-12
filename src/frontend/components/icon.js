class Icon {
  constructor(args) {
    this.element = document.getElementById(args.id);
    this.pathOff = "";
    this.pathOn = "";
    var img = document.createElement("img");
    img.src = "icons/" + this.pathOff;
    img.style.width = "100%";
    this.element.appendChild(img);
  }

  refresh(value) {
    var img = document.createElement("img");
    img.style.width = "100%";
    img.src = "icons/" + (value > 0 ? this.pathOn : this.pathOff);
    this.element.innerHTML = "";
    this.element.appendChild(img);
  }

  setPathoff(path) {
    this.pathOff = path;
  }

  setPathon(path) {
    this.pathOn = path;
  }
}
