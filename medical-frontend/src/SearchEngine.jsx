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
      overviewContainer.style.display = 'none'
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
    const btn = document.getElementById(encodeURIComponent(url))
    fetch('http://127.0.0.1:5000/api/summarize', {
      method: 'POST',
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({"query": url})
    }).then((res)=>{
      if(res.ok){
        return res.json()
      }
    }).then((data)=>{
      if(btn.childNodes[1].innerText != "v"){
        btn.childNodes[1].innerText = "v"
        btn.childNodes[0].innerText = ""
      }
      else{
        btn.childNodes[0].innerText = data["summary"]
        btn.childNodes[1].innerText = "^"
      }
    })
  }

  return (
      <div id='search-page'>
        <section class="search-area">
            <h1>HealthPro</h1>
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
                      <Link to={url} target="_blank">
                        {url}
                      </Link>
                      <div id = {encodeURIComponent(url)} class="output" onClick={() => Summarize(url)}>
                        <div></div>
                        <button>v</button>
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