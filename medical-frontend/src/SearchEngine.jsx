import search from '/search.png'
import './App.css'
import './SearchEngine.css'
import About from './About'
import Disclaimer from './Disclaimer'
import Overview from './Overview'
import { useState,useEffect } from 'react'
import {Link} from 'react-router-dom'
function SearchEngine() {
  const [output,setOutput] = useState([])

  const Search = (e) => {
    const searchbar = document.getElementById("searchbar")
    const overviewContainer = document.getElementById("overview-container")
    
    if(e.keyCode === 13 && document.activeElement === searchbar){
      overview.innerText = "Loading..."
      output.map((url)=>{
        const display = document.getElementById(encodeURIComponent(url))
        const btn = document.getElementById(encodeURIComponent(url)+"btn")
        btn.innerText = "v"
        display.innerText = ""
      })
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
        fetch('http://127.0.0.1:5000/api/cache', {
          method: 'POST',
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({})
        })
      })

      fetch('http://127.0.0.1:5000/api/query', {
        method: 'POST',
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({"query": searchbar.value})
      }).then((res)=>{
        if(res.ok){
          return res.json()
        }
      }).then((data)=>{
        const overview = document.getElementById("overview")
        overview.innerText = data["overview"]
        overviewContainer.style.display = "block"
      })
    }
  };

  const Summarize = (url) =>{
    const display = document.getElementById(encodeURIComponent(url))
    const btn = document.getElementById(encodeURIComponent(url)+"btn")
    if(btn.innerText != "v"){
      btn.innerText = "v"
      display.innerText = ""
    }
    else if (display.innerText != "Loading..."){
      display.innerText = "Loading..."
      fetch('http://127.0.0.1:5000/api/content', {
        method: 'POST',
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({"url": url})
      }).then((res)=>{
        if(res.ok){
          return res.json()
        }
      }).then((data)=>{
          display.innerText = data["summary"]
          btn.innerText = "^"
      })
    }
    
  }

  return (
      <div id='search-page'>
        <section class="search-area">
            <h1><Link to="/">HealthPro</Link></h1>
            <div class="input-container">
                <img src={search}></img>
                <input type="search" placeholder="what are the symptoms of covid-19..." class="input" id="searchbar" onKeyDown={Search}></input>
            </div>
            <ul class="output-container">
              <li id="overview-container">
                <strong>AI Overview</strong>
                <div id="overview">
                </div>
              </li>
              {output.map((url)=>{
                const urlpath = "/search-engine/"+encodeURIComponent(url);
                return(
                    <li>
                      <div class="result">
                          <Link to={url} target="_blank" class="url">
                            {url}
                          </Link>   
                        <button id = {encodeURIComponent(url)+"btn"} onClick={() => Summarize(url)}>v</button>
                      </div>
                      <div id = {encodeURIComponent(url)} class="output">
                      </div>
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