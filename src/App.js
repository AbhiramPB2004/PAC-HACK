import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ProductDetail from './components/Product_Creating';
import ProductCreating from './components/Product_Detail';

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<ProductDetail />} />
          <Route path="/create-product" element={<ProductCreating />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
