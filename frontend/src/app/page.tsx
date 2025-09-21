"use client";

import React from "react";
import { SparklesCore } from "@/components/ui/sparkles";
import { BackgroundRippleEffect } from "@/components/ui/background-ripple-effect";
import { AuroraText } from "@/components/ui/aurora-text";
import { TypewriterEffectSmooth } from "@/components/ui/typewriter-effect";
import { TypingAnimation } from "@/components/ui/typing-animation";
import { HoverBorderGradient } from "@/components/ui/hover-border-gradient";
import { ScrollReveal, StaggeredReveal } from "@/components/ui/scroll-reveal";
import { ArrowRight, Shield, Zap, Camera, Brain, Users, Award } from "lucide-react";
import { motion } from "framer-motion";
import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-black text-white overflow-hidden relative">
      {/* Consistent Black Background */}
      <div className="absolute inset-0 bg-black z-0"></div>
      {/* Background Ripple Effect - Only for Hero Section */}
      <div className="absolute top-0 left-0 right-0 h-[40rem] z-[1]">
        <BackgroundRippleEffect rows={25} cols={50} cellSize={35} />
      </div>

      {/* Floating Particles */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none z-[2]">
        {[...Array(20)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-1 h-1 bg-white/20 rounded-full"
            initial={{
              x: Math.random() * window.innerWidth,
              y: Math.random() * window.innerHeight,
            }}
            animate={{
              y: [null, -100, window.innerHeight + 100],
              opacity: [0, 1, 0],
            }}
            transition={{
              duration: Math.random() * 10 + 10,
              repeat: Infinity,
              delay: Math.random() * 5,
            }}
          />
        ))}
      </div>

      {/* Gradient Orbs */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-gradient-to-r from-cyan-500/5 to-purple-500/5 rounded-full blur-3xl animate-pulse pointer-events-none z-[2]"></div>
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-gradient-to-r from-purple-500/5 to-pink-500/5 rounded-full blur-3xl animate-pulse delay-1000 pointer-events-none z-[2]"></div>
      {/* Hero Section - Clean Grid + Text */}
      <div className="h-[40rem] w-full flex flex-col items-center justify-center overflow-hidden rounded-md relative">

        {/* Text Content */}
        <div className="relative z-[3] flex flex-col items-center text-center">
          <h1 className="md:text-7xl text-3xl lg:text-9xl font-bold text-center text-white mb-6 inline-flex items-baseline">
            <TypewriterEffectSmooth
              words={[
                { text: "LicensePlate", className: "text-white" },
              ]}
            />
            <AuroraText className="inline-block text-3xl md:text-7xl lg:text-9xl">AI</AuroraText>
          </h1>

          {/* Subtitle */}
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.8 }}
            className="text-neutral-300 text-lg md:text-xl text-center max-w-3xl mb-8"
          >
            Advanced AI-powered license plate recognition with real-time helmet detection.
            Revolutionizing traffic safety monitoring with cutting-edge computer vision technology.
          </motion.p>

          {/* CTA Button - Centered in Hero */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6, duration: 0.8 }}
            className="flex justify-center"
          >
            <Link href="/detect">
              <button className="bg-black hover:bg-gray-900 border border-white/20 hover:border-cyan-400/50 px-8 py-4 font-medium text-base flex items-center gap-3 group transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-cyan-400/30 rounded-xl relative overflow-hidden">
                <span className="text-white relative z-10">
                  Start Detection
                </span>
                <ArrowRight className="h-5 w-5 group-hover:translate-x-1 transition-all duration-300 text-white relative z-10" />
                <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/0 via-cyan-400/10 to-purple-500/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              </button>
            </Link>
          </motion.div>
        </div>
      </div>

      {/* Content Section */}
      <div className="relative z-[10] flex flex-col items-center text-center px-5 py-8 space-y-8">

        {/* Trusted By Section */}
        <div className="mb-16">
          <ScrollReveal direction="up" distance={20} duration={600} delay={900}>
            <p className="text-gray-400 text-sm mb-6">Trusted by traffic authorities worldwide</p>
          </ScrollReveal>
          <div className="flex flex-wrap justify-center items-center gap-8 opacity-60">
            <ScrollReveal direction="left" distance={30} duration={600} delay={1000} scale={0.9}>
              <div className="bg-white/5 px-6 py-3 rounded-lg border border-white/10">
                <span className="text-white font-medium">Traffic Police</span>
              </div>
            </ScrollReveal>
            <ScrollReveal direction="up" distance={30} duration={600} delay={1100} scale={0.9}>
              <div className="bg-white/5 px-6 py-3 rounded-lg border border-white/10">
                <span className="text-white font-medium">Highway Patrol</span>
              </div>
            </ScrollReveal>
            <ScrollReveal direction="right" distance={30} duration={600} delay={1200} scale={0.9}>
              <div className="bg-white/5 px-6 py-3 rounded-lg border border-white/10">
                <span className="text-white font-medium">Smart Cities</span>
              </div>
            </ScrollReveal>
          </div>
        </div>

        {/* Features Grid */}
        <ScrollReveal direction="up" distance={80} duration={1000} delay={100}>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl">
            <ScrollReveal direction="left" distance={60} duration={900} delay={200} scale={0.8}>
              <motion.div
                whileHover={{ y: -10, scale: 1.02 }}
                transition={{ type: "spring", stiffness: 300 }}
                className="bg-gradient-to-br from-black/40 to-black/20 backdrop-blur-md border border-white/10 rounded-3xl p-8 hover:border-cyan-400/30 transition-all duration-500 group shadow-2xl hover:shadow-cyan-400/10 relative overflow-hidden"
              >
                <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-cyan-400/10 to-transparent rounded-full blur-2xl"></div>
                <div className="bg-gradient-to-br from-cyan-500/20 to-blue-500/20 p-4 rounded-2xl w-fit mb-6 group-hover:scale-110 transition-all duration-300 relative z-10">
                  <Zap className="h-8 w-8 text-cyan-400" />
                </div>
                <h3 className="font-bold text-2xl mb-4 text-white relative z-10">Real-time Detection</h3>
                <p className="text-gray-300 leading-relaxed relative z-10">Instant license plate recognition with millisecond response times and 99.2% accuracy</p>
                <div className="mt-4 flex items-center gap-2 relative z-10">
                  <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                  <span className="text-green-400 text-sm font-medium">Live Processing</span>
                </div>
              </motion.div>
            </ScrollReveal>

            <ScrollReveal direction="up" distance={80} duration={900} delay={400} scale={0.8}>
              <motion.div
                whileHover={{ y: -10, scale: 1.02 }}
                transition={{ type: "spring", stiffness: 300 }}
                className="bg-gradient-to-br from-black/40 to-black/20 backdrop-blur-md border border-white/10 rounded-3xl p-8 hover:border-purple-400/30 transition-all duration-500 group shadow-2xl hover:shadow-purple-400/10 relative overflow-hidden"
              >
                <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-purple-400/10 to-transparent rounded-full blur-2xl"></div>
                <div className="bg-gradient-to-br from-purple-500/20 to-pink-500/20 p-4 rounded-2xl w-fit mb-6 group-hover:scale-110 transition-all duration-300 relative z-10">
                  <Shield className="h-8 w-8 text-purple-400" />
                </div>
                <h3 className="font-bold text-2xl mb-4 text-white relative z-10">Helmet Compliance</h3>
                <p className="text-gray-300 leading-relaxed relative z-10">Automated helmet detection for traffic safety enforcement with advanced computer vision</p>
                <div className="mt-4 flex items-center gap-2 relative z-10">
                  <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse"></div>
                  <span className="text-purple-400 text-sm font-medium">Safety First</span>
                </div>
              </motion.div>
            </ScrollReveal>

            <ScrollReveal direction="right" distance={60} duration={900} delay={600} scale={0.8}>
              <motion.div
                whileHover={{ y: -10, scale: 1.02 }}
                transition={{ type: "spring", stiffness: 300 }}
                className="bg-gradient-to-br from-black/40 to-black/20 backdrop-blur-md border border-white/10 rounded-3xl p-8 hover:border-green-400/30 transition-all duration-500 group shadow-2xl hover:shadow-green-400/10 relative overflow-hidden"
              >
                <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-green-400/10 to-transparent rounded-full blur-2xl"></div>
                <div className="bg-gradient-to-br from-green-500/20 to-emerald-500/20 p-4 rounded-2xl w-fit mb-6 group-hover:scale-110 transition-all duration-300 relative z-10">
                  <Brain className="h-8 w-8 text-green-400" />
                </div>
                <h3 className="font-bold text-2xl mb-4 text-white relative z-10">AI Powered</h3>
                <p className="text-gray-300 leading-relaxed relative z-10">Advanced YOLOv5 neural networks with machine learning algorithms for superior accuracy</p>
                <div className="mt-4 flex items-center gap-2 relative z-10">
                  <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                  <span className="text-green-400 text-sm font-medium">Smart Detection</span>
                </div>
              </motion.div>
            </ScrollReveal>
          </div>
        </ScrollReveal>
      </div>

      {/* Stats Section */}
      <section className="py-20 px-4 relative z-[10] bg-black">
        <div className="container mx-auto text-center">
          <ScrollReveal direction="up" distance={50} duration={800} delay={100}>
            <h2 className="text-3xl md:text-4xl font-bold mb-12">Trusted by Traffic Authorities</h2>
          </ScrollReveal>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <ScrollReveal direction="up" distance={40} duration={700} delay={200} scale={0.8}>
              <div className="text-center">
                <div className="text-3xl md:text-4xl font-bold text-indigo-400 mb-2">99.2%</div>
                <div className="text-neutral-400">Accuracy Rate</div>
              </div>
            </ScrollReveal>
            <ScrollReveal direction="up" distance={40} duration={700} delay={300} scale={0.8}>
              <div className="text-center">
                <div className="text-3xl md:text-4xl font-bold text-sky-400 mb-2">50ms</div>
                <div className="text-neutral-400">Processing Time</div>
              </div>
            </ScrollReveal>
            <ScrollReveal direction="up" distance={40} duration={700} delay={400} scale={0.8}>
              <div className="text-center">
                <div className="text-3xl md:text-4xl font-bold text-green-400 mb-2">1M+</div>
                <div className="text-neutral-400">Images Processed</div>
              </div>
            </ScrollReveal>
            <ScrollReveal direction="up" distance={40} duration={700} delay={500} scale={0.8}>
              <div className="text-center">
                <div className="text-3xl md:text-4xl font-bold text-purple-400 mb-2">24/7</div>
                <div className="text-neutral-400">Uptime</div>
              </div>
            </ScrollReveal>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 bg-black relative z-[10]">
        <div className="container mx-auto">
          <ScrollReveal direction="up" distance={60} duration={800} delay={100}>
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold mb-4">Advanced AI Capabilities</h2>
              <p className="text-neutral-400 text-lg max-w-2xl mx-auto">
                Our cutting-edge computer vision technology delivers unmatched performance in traffic monitoring and safety enforcement.
              </p>
            </div>
          </ScrollReveal>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <ScrollReveal direction="left" distance={50} duration={800} delay={200} scale={0.9}>
              <motion.div
                whileHover={{ scale: 1.05 }}
                className="bg-gradient-to-br from-neutral-900/50 to-neutral-800/30 backdrop-blur-sm border border-neutral-700 rounded-2xl p-8"
              >
                <Camera className="h-12 w-12 text-indigo-400 mb-4" />
                <h3 className="text-xl font-semibold mb-3">Multi-Object Detection</h3>
                <p className="text-neutral-400">Simultaneously detect vehicles, riders, helmets, and license plates in a single frame.</p>
              </motion.div>
            </ScrollReveal>

            <ScrollReveal direction="up" distance={60} duration={800} delay={400} scale={0.9}>
              <motion.div
                whileHover={{ scale: 1.05 }}
                className="bg-gradient-to-br from-neutral-900/50 to-neutral-800/30 backdrop-blur-sm border border-neutral-700 rounded-2xl p-8"
              >
                <Users className="h-12 w-12 text-sky-400 mb-4" />
                <h3 className="text-xl font-semibold mb-3">Rider Analysis</h3>
                <p className="text-neutral-400">Advanced algorithms to identify individual riders and their safety compliance status.</p>
              </motion.div>
            </ScrollReveal>

            <ScrollReveal direction="right" distance={50} duration={800} delay={600} scale={0.9}>
              <motion.div
                whileHover={{ scale: 1.05 }}
                className="bg-gradient-to-br from-neutral-900/50 to-neutral-800/30 backdrop-blur-sm border border-neutral-700 rounded-2xl p-8"
              >
                <Award className="h-12 w-12 text-green-400 mb-4" />
                <h3 className="text-xl font-semibold mb-3">OCR Technology</h3>
                <p className="text-neutral-400">State-of-the-art optical character recognition for accurate license plate reading.</p>
              </motion.div>
            </ScrollReveal>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 relative z-[10] bg-black">
        <div className="container mx-auto text-center">
          <ScrollReveal direction="up" distance={80} duration={1000} delay={100} scale={0.9}>
            <div className="bg-gradient-to-r from-indigo-600/20 to-purple-600/20 border border-indigo-500/20 rounded-3xl p-12">
              <ScrollReveal direction="up" distance={30} duration={800} delay={300}>
                <h2 className="text-3xl md:text-4xl font-bold mb-4">Ready to Get Started?</h2>
              </ScrollReveal>

              <ScrollReveal direction="up" distance={30} duration={800} delay={500}>
                <p className="text-neutral-300 text-lg mb-8 max-w-2xl mx-auto">
                  Experience the power of AI-driven traffic monitoring. Upload an image and see our technology in action.
                </p>
              </ScrollReveal>

              <ScrollReveal direction="up" distance={40} duration={800} delay={700} scale={0.9}>
                <Link href="/detect">
                  <button className="bg-black hover:bg-gray-900 border border-white/20 hover:border-blue-400/50 px-8 py-4 font-medium text-base flex items-center gap-3 group transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-blue-400/40 rounded-md mx-auto relative overflow-hidden">
                    <span className="text-white relative z-10">
                      Try Detection Now
                    </span>
                    <ArrowRight className="h-5 w-5 group-hover:translate-x-2 transition-all duration-300 text-white relative z-10" />
                    <div className="absolute inset-0 bg-gradient-to-r from-blue-500/0 via-blue-400/15 to-purple-500/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                  </button>
                </Link>
              </ScrollReveal>
            </div>
          </ScrollReveal>
        </div>
      </section>
    </main>
  );
}