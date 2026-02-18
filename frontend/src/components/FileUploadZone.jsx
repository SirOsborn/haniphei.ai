import React from "react";
import UploadIcon from "./icons/UploadIcon";

const FileUploadZone = ({ onFileChange }) => {
  return (
    <div>
      <div
        className="border-2 border-dashed border-primary/30 rounded-2xl p-12 text-center hover:border-primary/60 transition-all duration-300 glass cursor-pointer"
        onClick={() => document.getElementById("fileUpload").click()}
      >
        <UploadIcon className="w-20 h-20 mx-auto mb-4 text-primary" />
        <p className="text-lg font-medium text-white mb-2">
          Drop your legal document here
        </p>
        <p className="text-sm text-gray-400 mb-4">or click to browse</p>
        <input
          type="file"
          className="hidden"
          id="fileUpload"
          multiple
          onChange={onFileChange}
        />
        <button className="btn-secondary inline-block">Choose File</button>
      </div>
    </div>
  );
};

export default FileUploadZone;
