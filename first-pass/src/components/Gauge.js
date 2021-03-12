import './Gauge.css';

function Gauge() {
  let value = 112;
  let label = "LABEL";
  let backgroundColor = "#cc2c24";

  return (
      <div style={{backgroundColor: backgroundColor}} class="gauge">
        <p class="md:text-8xl font-black">{value}</p>
        <div>{label}</div>
      </div>
  );
}

export default Gauge;