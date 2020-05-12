class Text {
  constructor(args) {
    this.element = document.getElementById(args.id);
    this.prefix = args.prefix || "";
    this.suffix = args.suffix || "";

    this.element.innerHTML = this.prefix + args.value + this.suffix;
    this.element.style.fontSize = args.size + "vw";
    this.element.style.fontFamily = args.font || "arial";
    this.element.style.fontWeight = args.weight || "bold";
    this.element.style.fontStyle = args.style || "";
    this.element.style.textAlign = args.textAlign || "";
  }

  refresh(value) {
    this.element.innerHTML = this.prefix + value + this.suffix;
  }

  setSuffix(suffix) {
    if (suffix != null) {
      this.suffix = suffix;
    }
  }

  setColor(color) {
    this.element.style.color = color;
  }
}
