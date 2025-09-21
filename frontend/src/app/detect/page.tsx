"use client";

import React, { useState } from "react";
import { HeroSection } from "@/components/hero-section";
import { ResultsSection } from "@/components/results-section";
import { uploadAndAnalyzeImage, DetectionResponse } from "@/lib/api";
import { toast, Toaster } from "sonner";

export default function DetectPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<DetectionResponse | null>(null);

  const handleImageUpload = async (file: File) => {
    setIsLoading(true);
    
    try {
      const response = await uploadAndAnalyzeImage(file);
      setResult(response);
      
      if (response.success) {
        toast.success("Image analyzed successfully!");
      } else {
        toast.error(response.error || "Analysis failed");
      }
    } catch (error) {
      console.error("Upload error:", error);
      toast.error(error instanceof Error ? error.message : "Failed to analyze image");
    } finally {
      setIsLoading(false);
    }
  };

  const handleBack = () => {
    setResult(null);
  };

  return (
    <main className="min-h-screen bg-black">
      <Toaster 
        theme="dark" 
        position="top-right"
        toastOptions={{
          style: {
            background: '#1f2937',
            border: '1px solid #374151',
            color: '#f9fafb',
          },
        }}
      />
      
      {result ? (
        <ResultsSection result={result} onBack={handleBack} />
      ) : (
        <HeroSection onImageUpload={handleImageUpload} isLoading={isLoading} />
      )}
    </main>
  );
}