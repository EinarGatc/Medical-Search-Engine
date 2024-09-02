import React from 'react'
import ReactDOM from 'react-dom/client'
import Home from './Home.jsx'
import SearchEngine from './SearchEngine.jsx'
import Overview from './Overview.jsx'
import Error from './Error.jsx'
import {Route, Routes, Link, BrowserRouter} from 'react-router-dom'

ReactDOM.createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Home/>}></Route>
      <Route path="/search-engine" element={<SearchEngine/>}></Route>
      <Route path="/search-engine/:url" element={<Overview/>}></Route>
      <Route path="*" element={<Error/>}></Route>
    </Routes>
  </BrowserRouter>
)
