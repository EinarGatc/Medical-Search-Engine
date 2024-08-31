import search from '/search.png'
import './App.css'
import './SearchEngine.css'
import About from './About'
import Disclaimer from './Disclaimer'
import { useState,useEffect } from 'react'
import {Link} from 'react-router-dom'
function SearchEngine() {
  const [output,setOutput] = useState([])

  const Search = (e) => {
    const searchbar = document.getElementById("searchbar")
    const container = document.getElementsByClassName("output-container")
    
    if(e.keyCode === 13 && document.activeElement === searchbar){
      fetch('http://127.0.0.1:5000/api/urls', {
        method: 'POST',
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({"query": searchbar.value})
      }).then((res)=>{
        if(res.ok){
          return res.json()
        }
      }).then((data)=>{
        const urls = data["urls"]
        setOutput(urls)
      })
    }
  };

  return (
      <div id='search-page'>
        <section class="search-area">
            <h1>HealthPro</h1>
            <div class="input-container">
                <img src={search}></img>
                <input type="search" placeholder="what are the symptoms of covid-19..." class="input" id="searchbar" onKeyDown={Search}></input>
            </div>
            <ul class="output-container">
              {output.map((url)=>{
                return(
                <li><Link to={url} target="_blank">
                  {url}
                  </Link>
                </li>
                )
              })}
            </ul>
            <Disclaimer></Disclaimer>
        </section>
        <About></About>
      </div>
  )
}

export default SearchEngine