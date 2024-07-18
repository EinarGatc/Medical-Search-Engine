import search from '/search.png'
import './App.css'
import './SearchEngine.css'
import About from './About'
import Disclaimer from './Disclaimer'
function SearchEngine() {

  return (
      <div id='search-page'>
        <section class="search-area">
            <h1>HealthPro</h1>
            <div class="input-container">
                <img src={search}></img>
                <input type="search" placeholder="what are the symptoms of covid-19..." class="input"></input>
            </div>
            <ul class="output-container">
            </ul>
            <Disclaimer></Disclaimer>
        </section>
        <About></About>
      </div>
  )
}

export default SearchEngine