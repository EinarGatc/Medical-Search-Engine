import { useParams, Link } from "react-router-dom";

function Overview() {
    const params = useParams()
    const url = decodeURIComponent(params.url)
    return (
        <div id="overview-page">
            <div class="description"></div>
            <div class="summary"></div>
            <Link to={url} target="_blank">
                {url}
            </Link>
        </div>
    )
  }
  
  export default Overview