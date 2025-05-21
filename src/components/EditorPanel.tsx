
import React, { useState, useRef, useEffect } from 'react';
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { Play, Pause, Save, Upload, FileText, Book } from "lucide-react";

interface EditorPanelProps {
  dyslexicMode: boolean;
}

const EditorPanel = ({ dyslexicMode }: EditorPanelProps) => {
  const [text, setText] = useState<string>("Enter your script here...");
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [currentWordIndex, setCurrentWordIndex] = useState<number>(-1);
  const [playbackRate, setPlaybackRate] = useState<number>(1);
  const wordsRef = useRef<string[]>([]);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setText(e.target.value);
    wordsRef.current = e.target.value.split(/\s+/);
  };

  const togglePlayback = () => {
    if (isPlaying) {
      stopPlayback();
    } else {
      startPlayback();
    }
  };

  const startPlayback = () => {
    setIsPlaying(true);
    setCurrentWordIndex(0);
  };

  const stopPlayback = () => {
    setIsPlaying(false);
    setCurrentWordIndex(-1);
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
  };

  // Simulate TTS playback with word highlighting
  useEffect(() => {
    if (isPlaying && currentWordIndex >= 0) {
      if (currentWordIndex < wordsRef.current.length) {
        // Play next word after delay (simulating TTS)
        const wordDelay = 250 / playbackRate; // Faster rate = shorter delay
        timeoutRef.current = setTimeout(() => {
          setCurrentWordIndex(prev => prev + 1);
        }, wordDelay);
      } else {
        // End of text
        stopPlayback();
      }
    }
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [isPlaying, currentWordIndex, playbackRate]);

  useEffect(() => {
    // Initialize words on component mount
    wordsRef.current = text.split(/\s+/);
  }, []);

  // Render text with highlighted current word
  const renderText = () => {
    if (currentWordIndex === -1) return text;
    
    const words = text.split(/\s+/);
    return words.map((word, index) => (
      <span 
        key={index} 
        className={index === currentWordIndex ? "highlighted-word" : ""}
      >
        {word}{' '}
      </span>
    ));
  };

  return (
    <div className="flex flex-col h-full w-full">
      <div className="flex-1 relative">
        {isPlaying ? (
          <div 
            className={`editor-container overflow-y-auto ${dyslexicMode ? 'font-dyslexic' : 'font-inter'}`}
          >
            {renderText()}
          </div>
        ) : (
          <textarea
            className={`editor-container resize-none ${dyslexicMode ? 'font-dyslexic' : 'font-inter'}`}
            value={text}
            onChange={handleTextChange}
            placeholder="Enter your script here..."
          />
        )}
      </div>
      
      <div className="flex flex-col space-y-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex space-x-2">
            <Button 
              onClick={togglePlayback}
              variant="default"
              size="icon"
              className="bg-scriptRed hover:bg-scriptRed/80"
            >
              {isPlaying ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
            </Button>
            <Button 
              variant="outline"
              size="icon" 
              className="border-scriptRed/50 text-white"
            >
              <Save className="h-4 w-4" />
            </Button>
            <Button 
              variant="outline" 
              size="icon"
              className="border-scriptRed/50 text-white"
            >
              <Upload className="h-4 w-4" />
            </Button>
          </div>
          
          <div className="flex items-center space-x-2">
            <FileText className="h-4 w-4 text-scriptRed" />
            <span className="text-sm text-white">Words: {wordsRef.current.length}</span>
          </div>
        </div>
        
        <div className="flex items-center space-x-4">
          <Book className="h-4 w-4 text-scriptRed" />
          <span className="text-sm text-white">Speed:</span>
          <Slider
            value={[playbackRate]}
            min={0.5}
            max={2}
            step={0.1}
            onValueChange={(values) => setPlaybackRate(values[0])}
            className="w-32"
          />
          <span className="text-sm text-white">{playbackRate.toFixed(1)}x</span>
        </div>
      </div>
    </div>
  );
};

export default EditorPanel;
