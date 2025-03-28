"use client";

import { useState } from "react";
import {motion, useAnimationControls} from "framer-motion";



export default function EnterPage() {
  const [invokeComplete, setInvokeComplete] = useState(false);
  const controls = useAnimationControls();


  const handleUpload = async () => {
    const response = await fetch("http://localhost:5000/run-script", {
      method: "POST",
    });
    const data = await response.json();
    alert(data.message);
  };

  



    const [playlistUrl, setPlaylistUrl] = useState("");
  
    const handlePlaylist = async () => {
      if (!playlistUrl) {
        alert("Please enter a playlist URL");
        return;
      }
  
      const response = await fetch("http://localhost:5000/playlist", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: playlistUrl }),
      });

      const data = await response.json();
      alert(data.message);


    };
 







  const handleInvoke = async () => {
    setInvokeComplete(false);
    const response = await fetch("http://localhost:5000/invoke", {
      method: "POST",
    });
    const data = await response.json();
    alert(data.message);
        setInvokeComplete(true);
  };


  return (
<div className="flex w-full h-screen font-[Poppins]">
  {/* Left Section (Controls) */}
  <div className="w-1/2 flex flex-col gap-6 p-8 text-gray-800">
    <motion.button
      whileTap={{
        scale: 0.75,
      }}
      onClick={handleUpload}
      className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white/90 rounded-lg shadow-lg transition-transform transform hover:scale-105 w-48"
    >
      Upload Liked Songs
    </motion.button>

    <motion.input
    variants={{
      initial: { width: "12rem" },
      expand: { width: "50%" },
    }}
    onFocus={()=>controls.start("expand")}
    onBlur={()=>controls.start("initial")}
    initial="initial"
    animate={controls}
      type="text"
      placeholder="Enter playlist URL"
      value={playlistUrl}
      onChange={(e) => setPlaylistUrl(e.target.value)}
      className="px-4 py-3 border border-gray-300 rounded-lg w-1/2 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 text-white font-bold"
    />

    <motion.button
    whileTap={{
      scale: 0.75,
    }}
      onClick={handlePlaylist}
      className="px-6 py-3 bg-gradient-to-r from-green-500 to-blue-600 text-white/90 rounded-lg shadow-lg transition-transform transform hover:scale-105 w-48"
    >
      Upload Playlist
    </motion.button>

    <motion.button
    whileTap={{
      scale: 0.85,
    }}
      onClick={handleInvoke}
      className="px-6 py-3 bg-gradient-to-r from-pink-600 to-red-600 text-white/90 rounded-lg shadow-lg transition-transform transform hover:scale-105 w-48"
    >
      Invoke
    </motion.button>
  </div>

  {/* Separator Line */}
  <div className="w-0.5 bg-gray-300 h-5/6"></div>

  {/* Right Section (Audio Output) */}
  <div className="w-1/2 flex items-center justify-center">
    {invokeComplete && (
      <div className="p-6 w-2xl bg-gray-100 rounded-lg shadow-lg">
        <audio controls className="w-full">
          <source src="http://localhost:5000/musicgen_out.wav" type="audio/wav" />
          Your browser does not support the audio element.
        </audio>
      </div>
    )}
  </div>
</div>


  );
}
