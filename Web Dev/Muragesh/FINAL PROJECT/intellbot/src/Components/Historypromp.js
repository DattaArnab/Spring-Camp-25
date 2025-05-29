import React from 'react'
import ("./Promp.css")

function Historypromp(props) {
  return (
    <div className='apromp'> 
    <h4 style={{color:"#b5d8f2"}} >{props.msg}</h4>
    <h6 style={{position:"relative",left:"13rem",top:"-.2rem",color:"#b5d8f2"}}>{props.tim}</h6>
      
    </div>
  )
}

export default Historypromp
