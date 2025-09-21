"use client";

import React, { useState } from "react";

import { Upload, Camera, Shield, Zap, ArrowLeft } from "lucide-react";
import { motion } from "framer-motion";
import Link from "next/link";


interface HeroSectionProps {
  onImageUpload: (file: File) => void;
  isLoading?: boolean;
}

export function HeroSection({ onImageUpload, isLoading = false }: HeroSectionProps) {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (file.type.startsWith('image/')) {
        setSelectedFile(file);
        onImageUpload(file);
      }
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      onImageUpload(file);
    }
  };

  return (
    <div className="h-screen w-full bg-black flex flex-col items-center justify-center overflow-hidden relative">
      {/* Back Button */}
      <div className="absolute top-8 left-8 z-30">
        <Link href="/">
          <button className="flex items-center gap-2 px-4 py-2 bg-neutral-900/50 backdrop-blur-sm border border-neutral-700 rounded-lg hover:bg-neutral-800/50 transition-all duration-300">
            <ArrowLeft className="h-4 w-4" />
            Back to Home
          </button>
        </Link>
      </div>

      {/* Main Content */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="relative z-20 flex flex-col items-center"
      >
        {/* Title - Clean Design */}
        <div className="mb-8">
          <h1 className="md:text-6xl text-3xl lg:text-7xl font-bold text-center text-white">
            AI Detection
          </h1>
        </div>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3, duration: 0.8 }}
          className="text-neutral-300 text-lg md:text-xl text-center mb-12 max-w-2xl px-4"
        >
          Upload an image to analyze license plates and helmet compliance with our advanced AI system.
        </motion.p>

        {/* Upload Area */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.6, duration: 0.8 }}
          className="relative"
        >
          <div
            className={`
              relative w-96 h-64 border-2 border-dashed rounded-2xl
              bg-black/20 backdrop-blur-sm transition-all duration-300
              ${dragActive
                ? 'border-indigo-400 bg-indigo-500/10'
                : selectedFile
                  ? 'border-green-400 bg-green-500/10'
                  : 'border-neutral-600 hover:border-neutral-400'
              }
              ${isLoading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
            `}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <input
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              disabled={isLoading}
            />

            <div className="flex flex-col items-center justify-center h-full p-8">
              {isLoading ? (
                <div className="flex flex-col items-center">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500 mb-4"></div>
                  <p className="text-white font-medium">Processing...</p>
                  <p className="text-neutral-400 text-sm mt-2">Analyzing image with AI...</p>
                </div>
              ) : selectedFile ? (
                <div className="flex flex-col items-center">
                  <Camera className="h-12 w-12 text-green-400 mb-4" />
                  <p className="text-white font-medium mb-2">File Selected</p>
                  <p className="text-neutral-400 text-sm text-center">{selectedFile.name}</p>
                  <p className="text-green-400 text-xs mt-2">Processing will start automatically...</p>
                </div>
              ) : (
                <div className="flex flex-col items-center">
                  <Upload className="h-12 w-12 text-neutral-400 mb-4" />
                  <p className="text-white font-medium mb-2">Upload Image</p>
                  <p className="text-neutral-400 text-sm text-center">
                    Drag and drop or click to select<br />
                    Supports JPG, PNG, GIF (Max 10MB)
                  </p>
                </div>
              )}
            </div>
          </div>
        </motion.div>

        {/* Features */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.9, duration: 0.8 }}
          className="flex flex-wrap justify-center gap-8 mt-12"
        >
          <div className="flex items-center gap-2 text-neutral-300">
            <Zap className="h-5 w-5 text-indigo-400" />
            <span>Real-time Detection</span>
          </div>
          <div className="flex items-center gap-2 text-neutral-300">
            <Shield className="h-5 w-5 text-sky-400" />
            <span>Helmet Compliance</span>
          </div>
          <div className="flex items-center gap-2 text-neutral-300">
            <Camera className="h-5 w-5 text-green-400" />
            <span>High Accuracy</span>
          </div>
        </motion.div>
      </motion.div>
    </div>
  );
}