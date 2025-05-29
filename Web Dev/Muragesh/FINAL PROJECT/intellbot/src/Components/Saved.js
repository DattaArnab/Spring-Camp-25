import React,{useState} from 'react'
import("./Saved.css")
function Saved(props) {
    const [displayy,setDisplayy]=useState("none")
    const toggledisplay=()=>{
        setDisplayy("none")
    }
  return (
   <div className='saved' style={{ display: displayy }}>

        <button onClick={toggledisplay}></button>
      
    </div>
  )
}

export default Saved
