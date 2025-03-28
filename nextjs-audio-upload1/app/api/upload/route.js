import { NextResponse } from "next/server";
import { writeFile, readdir, unlink } from "fs/promises";
import path from "path";
import { mkdir } from "fs/promises";

export async function POST(req) {
  try {
    const uploadDir = path.join(process.cwd(), "public/uploads");
    
    // Ensure the uploads directory exists
    await mkdir(uploadDir, { recursive: true });

    // Delete existing files in the directory
    const existingFiles = await readdir(uploadDir);
    for (const file of existingFiles) {
      await unlink(path.join(uploadDir, file));
    }

    // Extract files from FormData
    const formData = await req.formData();
    const files = formData.getAll("files"); // Get all uploaded files

    if (!files.length) {
      return NextResponse.json({ message: "No files uploaded" }, { status: 400 });
    }

    let uploadedFiles = [];

    for (const file of files) {
      const fileBuffer = Buffer.from(await file.arrayBuffer());
      const filePath = path.join(uploadDir, file.name);
      
      // Save the file
      await writeFile(filePath, fileBuffer);
      uploadedFiles.push(filePath);
    }

    return NextResponse.json({ message: "Files uploaded successfully", uploadedFiles });
  } catch (error) {
    console.error("Upload error:", error);
    return NextResponse.json({ message: "Upload failed", error: error.message }, { status: 500 });
  }
}