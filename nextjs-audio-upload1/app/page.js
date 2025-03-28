import Link from "next/link";

export default function Home() {
  return (
    <div className="relative min-h-screen text-white">
      {/* Background GIF */}
      <div className="absolute inset-0 z-0">
        <img
          src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExNnB6YnJmOWVyM3NqMmxqZ3pqMG05MmExaGYweDRzNXl6d2tnZzRndyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jaOXKCxtBPLieRLI0c/giphy.gif"
          className="w-full h-full object-cover"
          alt="Background GIF"
        />
      </div>

      {/* Main Content (Ensures it is above the image) */}
      <div className="relative z-10 flex flex-col items-center justify-center min-h-screen p-6 text-center">
        <h1 className="text-6xl font-extrabold drop-shadow-lg mb-6 animate-fade-in">
          Welcome to{" "}
          <span className="text-yellow-300">
            Enhanced personalized music generation
          </span>
        </h1>
        <p className="text-xl font-light text-gray-100 mb-8 max-w-2xl">
          Upload and manage your files with ease, security, and style.
        </p>
        <div className="flex space-x-6">
          <Link href="/upload">
            <button className="bg-yellow-300 text-purple-700 px-8 py-4 text-lg rounded-full shadow-lg hover:bg-yellow-400 transition-all transform hover:scale-105">
              Upload via files
            </button>
          </Link>
          <Link href="/user">
            <button className="bg-blue-500 text-white px-8 py-4 text-lg rounded-full shadow-lg hover:bg-blue-600 transition-all transform hover:scale-105">
              Upload via User
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
}
