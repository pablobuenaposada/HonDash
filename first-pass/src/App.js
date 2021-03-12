import Gauge from './components/Gauge';
import Icon from './components/Icon';
import Bar from './components/Bar';
import Speed from './components/Speed';

function App() {
  return (
    <div className="App">
      <header className="App-header">
          <div class="w-full h-1"></div>

          <div class="flex h-24">
                <div class="w-1/6"></div>
                <Bar/>
                <div class="w-1/6"></div>
            </div>
          <div class="flex italic">
            <Speed/>
          </div>

          <div class="grid grid-cols-6 gap-2 text-center overflow-hidden" style={{padding: "0 5px 0"}}>
            <div><Gauge/></div>
            <div><Gauge/></div>
            <div><Gauge/></div>
            <div><Gauge/></div>
            <div><Gauge/></div>
            <div><Gauge/></div>
            <div><Gauge/></div>
            <div><Gauge/></div>
            <div><Gauge/></div>
            <div><Gauge/></div>
            <div><Gauge/></div>
            <div><Gauge/></div>
        </div>

          <div><Icon/></div>

          <div class="w-full h-3 text-center" style={{border: "1px solid red"}}>kpro version</div>

      </header>
    </div>
  );
}

export default App;
