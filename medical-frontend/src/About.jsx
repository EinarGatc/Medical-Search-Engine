import github from '/github.png'
import linkedin from '/linkedin.png'
import email from '/email.png'

function About() {

  return (
      <footer class="about section">
        <h3>About</h3>
        <p>HealthPro aims to make reliable health information more accessible by aggregating data from trusted medical websites.</p>
        <p>Created by Einar Gatchalian, Jason Nguyen, and Hearty Parrenas.</p>
        <div class="contacts">
          <img src={github}></img>
          <img src={linkedin}></img>
          <img src={email}></img>
        </div>
      </footer>
  )
}

export default About