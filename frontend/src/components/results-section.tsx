"use client";

import React, { useState } from "react";
import { motion } from "framer-motion";
import { ArrowLeft, Download, AlertTriangle, CheckCircle, Camera } from "lucide-react";

// Component to handle image loading with multiple fallback attempts
function ImageWithFallback({ imageUrl, alt }: { imageUrl: string; alt: string }) {
  const [currentAttempt, setCurrentAttempt] = useState(0);
  const [hasError, setHasError] = useState(false);

  const getImageUrl = (attempt: number) => {
    const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    
    // Debug: log the original imageUrl
    if (attempt === 0) {
      console.log('Original image URL from backend:', imageUrl);
    }
    
    switch (attempt) {
      case 0:
        // Try the original URL as provided by Django
        const url = imageUrl.startsWith('http') ? imageUrl : `${baseUrl}${imageUrl}`;
        console.log(`Attempt ${attempt + 1}: ${url}`);
        return url;
      case 1:
        // Try test static file to verify Django is serving static files
        const testUrl = `${baseUrl}/static/test.txt`;
        console.log(`Attempt ${attempt + 1} (test): ${testUrl}`);
        return testUrl;
      default:
        return imageUrl;
    }
  };

  const handleError = () => {
    // Log failed attempt for debugging
    if (process.env.NODE_ENV === 'development') {
      // eslint-disable-next-line no-console
      console.error(`Image load attempt ${currentAttempt + 1} failed:`, getImageUrl(currentAttempt));
    }
    
    if (currentAttempt < 1) {
      setCurrentAttempt(currentAttempt + 1);
    } else {
      setHasError(true);
    }
  };

  if (hasError) {
    return (
      <div className="w-full h-48 flex items-center justify-center text-neutral-400 flex-col">
        <Camera className="h-12 w-12 mb-2" />
        <p>Failed to load image</p>
        <p className="text-xs mt-1 text-center">
          Original URL: {imageUrl}<br/>
          Last attempt: {getImageUrl(currentAttempt)}
        </p>
        <div className="mt-2 space-y-2">
          <button 
            type="button"
            onClick={() => {
              // Test Django server connection
              console.log('Testing Django server...');
              fetch('http://localhost:8000/static/test.txt')
                .then(response => {
                  console.log('Static file test:', response.status, response.statusText);
                  return response.text();
                })
                .then(text => console.log('Test file content:', text))
                .catch(err => console.error('Static file test failed:', err));
            }}
            className="px-3 py-1 bg-blue-600 text-white text-xs rounded mr-2"
          >
            Test Static Files
          </button>
          <button 
            type="button"
            onClick={() => {
              // Test Django admin (should always work if Django is running)
              console.log('Testing Django admin...');
              fetch('http://localhost:8000/admin/')
                .then(response => {
                  console.log('Django admin test:', response.status, response.statusText);
                  console.log('Django server is running!');
                })
                .catch(err => {
                  console.error('Django server is NOT running:', err);
                  console.log('Please start Django server with: python manage.py runserver');
                });
            }}
            className="px-3 py-1 bg-green-600 text-white text-xs rounded"
          >
            Test Django Server
          </button>
        </div>
      </div>
    );
  }

  return (
    <img
      key={currentAttempt} // Force re-render on URL change
      src={getImageUrl(currentAttempt)}
      alt={alt}
      className="w-full h-auto max-h-96 object-contain"
      onError={handleError}
    />
  );
}

interface DetectionResult {
  image_url: string;
  detections: string;
  riders_without_helmets?: string[];
  processing_time?: number;
}

interface ResultsSectionProps {
  result: DetectionResult;
  onBack: () => void;
}

export function ResultsSection({ result, onBack }: ResultsSectionProps) {
  const hasViolations = result.riders_without_helmets && result.riders_without_helmets.length > 0;

  return (
    <div className="min-h-screen w-full bg-black text-white relative overflow-hidden">
      {/* Background Effects */}
      <div className="absolute inset-0 bg-gradient-to-br from-black via-neutral-900 to-black"></div>
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(99,102,241,0.1),transparent_50%)]"></div>

      <div className="relative z-10 container mx-auto px-4 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center justify-between mb-8"
        >
          <button
            type="button"
            onClick={onBack}
            className="bg-black hover:bg-gray-900 border border-white/20 hover:border-cyan-400/50 px-6 py-3 font-medium text-sm flex items-center gap-2 group transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-cyan-400/30 rounded-md relative overflow-hidden"
          >
            <ArrowLeft className="h-4 w-4 group-hover:-translate-x-1 transition-all duration-300 text-white relative z-10" />
            <span className="text-white relative z-10">Back to Upload</span>
            <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/0 via-cyan-400/10 to-purple-500/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          </button>
          
          <h1 className="text-2xl md:text-3xl font-bold">Detection Results</h1>
          
          <button 
            type="button"
            className="bg-black hover:bg-gray-900 border border-white/20 hover:border-blue-400/50 px-6 py-3 font-medium text-sm flex items-center gap-2 group transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-blue-400/30 rounded-md relative overflow-hidden"
          >
            <Download className="h-4 w-4 text-white relative z-10" />
            <span className="text-white relative z-10">Export</span>
            <div className="absolute inset-0 bg-gradient-to-r from-blue-500/0 via-blue-400/10 to-purple-500/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          </button>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Image Display */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="space-y-4"
          >
            <div className="bg-neutral-900/50 backdrop-blur-sm rounded-2xl p-6 border border-neutral-800">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Camera className="h-5 w-5 text-indigo-400" />
                Analyzed Image
              </h2>
              
              <div className="relative rounded-xl overflow-hidden bg-neutral-800">
                {result.image_url ? (
                  <ImageWithFallback 
                    imageUrl={result.image_url}
                    alt="Analyzed image"
                  />
                ) : (
                  <div className="w-full h-48 flex items-center justify-center text-neutral-400 flex-col">
                    <Camera className="h-12 w-12 mb-2" />
                    <p>No image available</p>
                  </div>
                )}
                <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent"></div>
              </div>
              
              <div className="mt-2 space-y-1">
                {result.processing_time && (
                  <p className="text-sm text-neutral-400">
                    Processing time: {result.processing_time}ms
                  </p>
                )}
                <p className="text-xs text-neutral-500">
                  Image URL: {result.image_url || 'Not provided'}
                </p>
              </div>
            </div>
          </motion.div>

          {/* Results Panel */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
            className="space-y-6"
          >
            {/* Status Overview */}
            <div className={`
              bg-gradient-to-r p-6 rounded-2xl border
              ${hasViolations 
                ? 'from-red-500/10 to-orange-500/10 border-red-500/20' 
                : 'from-green-500/10 to-emerald-500/10 border-green-500/20'
              }
            `}>
              <div className="flex items-center gap-3 mb-3">
                {hasViolations ? (
                  <AlertTriangle className="h-6 w-6 text-red-400" />
                ) : (
                  <CheckCircle className="h-6 w-6 text-green-400" />
                )}
                <h2 className="text-xl font-semibold">
                  {hasViolations ? 'Violations Detected' : 'All Clear'}
                </h2>
              </div>
              
              <p className={`text-sm ${hasViolations ? 'text-red-300' : 'text-green-300'}`}>
                {hasViolations 
                  ? `${result.riders_without_helmets?.length || 0} rider(s) without helmet detected`
                  : 'All riders are wearing helmets'
                }
              </p>
            </div>

            {/* Detection Details */}
            <div className="bg-neutral-900/50 backdrop-blur-sm rounded-2xl p-6 border border-neutral-800">
              <h3 className="text-lg font-semibold mb-4">Detection Details</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="text-sm text-neutral-400 block mb-1">Raw Detection Output</label>
                  <div className="bg-neutral-800 rounded-lg p-3 font-mono text-sm">
                    {result.detections || 'No specific detections reported'}
                  </div>
                </div>

                {result.riders_without_helmets && result.riders_without_helmets.length > 0 && (
                  <div>
                    <label className="text-sm text-neutral-400 block mb-2">Helmet Violations</label>
                    <div className="space-y-2">
                      {result.riders_without_helmets.map((rider, index) => (
                        <div
                          key={index}
                          className="bg-red-500/10 border border-red-500/20 rounded-lg p-3"
                        >
                          <div className="flex items-center gap-2">
                            <AlertTriangle className="h-4 w-4 text-red-400" />
                            <span className="text-red-300">{rider}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Actions */}
            <div className="bg-neutral-900/50 backdrop-blur-sm rounded-2xl p-6 border border-neutral-800">
              <h3 className="text-lg font-semibold mb-4">Actions</h3>
              
              <div className="grid grid-cols-2 gap-3">
                <button 
                  type="button"
                  className="bg-black hover:bg-gray-900 border border-white/20 hover:border-indigo-400/50 px-4 py-2 font-medium text-sm transition-all duration-300 hover:scale-105 hover:shadow-lg hover:shadow-indigo-400/20 rounded-md relative overflow-hidden group"
                >
                  <span className="text-white relative z-10">Save Report</span>
                  <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/0 via-indigo-400/10 to-purple-500/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                </button>
                <button 
                  type="button"
                  className="bg-black hover:bg-gray-900 border border-white/20 hover:border-gray-400/50 px-4 py-2 font-medium text-sm transition-all duration-300 hover:scale-105 hover:shadow-lg hover:shadow-gray-400/20 rounded-md relative overflow-hidden group"
                >
                  <span className="text-white relative z-10">Share Results</span>
                  <div className="absolute inset-0 bg-gradient-to-r from-gray-500/0 via-gray-400/10 to-gray-500/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                </button>
                <button 
                  type="button"
                  className="bg-black hover:bg-gray-900 border border-white/20 hover:border-green-400/50 px-4 py-2 font-medium text-sm transition-all duration-300 hover:scale-105 hover:shadow-lg hover:shadow-green-400/20 rounded-md relative overflow-hidden group"
                >
                  <span className="text-white relative z-10">Export Data</span>
                  <div className="absolute inset-0 bg-gradient-to-r from-green-500/0 via-green-400/10 to-emerald-500/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                </button>
                <button 
                  type="button"
                  className="bg-black hover:bg-gray-900 border border-white/20 hover:border-orange-400/50 px-4 py-2 font-medium text-sm transition-all duration-300 hover:scale-105 hover:shadow-lg hover:shadow-orange-400/20 rounded-md relative overflow-hidden group"
                >
                  <span className="text-white relative z-10">Flag Issue</span>
                  <div className="absolute inset-0 bg-gradient-to-r from-orange-500/0 via-orange-400/10 to-red-500/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                </button>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}