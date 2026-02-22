import React, { useState, useRef, useEffect } from "react";
import UploadIcon from "./icons/UploadIcon";

const FileUploadZone = ({ onFileChange }) => {
  const [isDragging, setIsDragging] = useState(false);
  const inputRef = useRef(null);
  const dragCounter = useRef(0);

  // Prevent browser from opening the file when dropped outside the zone
  useEffect(() => {
    const prevent = (e) => {
      e.preventDefault();
      e.stopPropagation();
    };
    window.addEventListener("dragover", prevent);
    window.addEventListener("drop", prevent);
    return () => {
      window.removeEventListener("dragover", prevent);
      window.removeEventListener("drop", prevent);
    };
  }, []);

  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    dragCounter.current += 1;
    setIsDragging(true);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    dragCounter.current -= 1;
    if (dragCounter.current === 0) {
      setIsDragging(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    dragCounter.current = 0;
    setIsDragging(false);
    const droppedFiles = e.dataTransfer.files;
    if (droppedFiles && droppedFiles.length > 0) {
      const syntheticEvent = { target: { files: droppedFiles } };
      onFileChange(syntheticEvent);
    }
  };

  return (
    <div
      onDragEnter={handleDragEnter}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      onClick={() => inputRef.current.click()}
      className={`border-2 border-dashed rounded-2xl p-12 text-center transition-all duration-300 glass cursor-pointer ${
        isDragging
          ? "border-primary bg-primary/10 scale-[1.01]"
          : "border-primary/30 hover:border-primary/60"
      }`}
    >
      <UploadIcon
        className={`w-20 h-20 mx-auto mb-4 transition-colors ${isDragging ? "text-primary" : "text-primary/70"}`}
      />
      <p className="text-lg font-medium text-white mb-2">
        {isDragging ? "Release to upload" : "Drop your legal document here"}
      </p>
      <p className="text-sm text-gray-400 mb-4">or click to browse</p>
      <input
        ref={inputRef}
        type="file"
        className="hidden"
        multiple
        onChange={onFileChange}
      />
      <button
        type="button"
        onClick={(e) => {
          e.stopPropagation();
          inputRef.current.click();
        }}
        className="btn-secondary inline-block"
      >
        Choose File
      </button>
    </div>
  );
};

export default FileUploadZone;
