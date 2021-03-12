import './Bar.css';

function Bar() {
  let backgroundColor = "yellow";
  let height = 100;
  let width = "100%";

  return (
      <div class="barparent w-4/6">
        <div style={{backgroundColor: backgroundColor, width: width}} class="bar h-full"></div>
      </div>
  );
}

export default Bar;