import medicalImage from '/trafalgar-header_illustration_1.webp'
import computer from '/computer.png'
import www from '/www.png'
import logic from '/logic.png'
import About from './About'
import Disclaimer from './Disclaimer'
import './App.css'
import './Home.css'
import {Link} from 'react-router-dom'

function App() {

  return (
    <div id="home-page">
      <nav id="navbar">
        <ul>
          <li class="home-button"><Link to="/">Home</Link></li>
          <li class="search-button"><Link to="/search-engine">Search Engine</Link></li>
        </ul>
      </nav>
      <div class="hero section">
        <section class="head">
          <h1>HealthPro</h1>
          <h2>Medical Search Engine</h2>
          <p>Discover accurate and up-to-date health information with HealthPro Search Engine</p>
          <button>Get Started</button>
        </section>
        <img src={medicalImage}></img>
      </div>
      <section class="how-it-works section">
        <h1>How it Works</h1>
        <p>
          Our search engine pulls data from top medical and health websites including MedlinePlus, 
          NCBI, CDC, Mayo Clinic, Merck Manuals, NNLM, Testing.com, and AHRQ, ensuring you receive 
          accurate and up-to-date information for all your health-related queries
        </p>
        <ul class="cards">
          <li>
            <h3>Webcrawler</h3>
            <img src={computer}></img>
          </li>
          <li>
            <h3>Search Engine</h3>
            <img src={www}></img>
          </li>
          <li>
            <h3>OpenAI API</h3>
            <img src={logic}></img>
          </li>
        </ul>
        <Disclaimer></Disclaimer>
      </section>
      <section class="how-to-use section">
        <h1>How to Use</h1>
        <ol>
          <li>Enter Your Query: Type your health-related question or keywords into the search bar.</li>
          <li>Press Search: Click the search button or press Enter to begin your search.</li>
          <li>Browse Results: Review the search results from trusted medical websites.</li>
          <li>Select an Article: Click on any result to read more about the topic on the original website.</li>
          <li>Refine Your Search: If needed, modify your query and search again to find more specific information.</li>
        </ol>
      </section>
      <About></About>
    </div>
  )
}

export default App
