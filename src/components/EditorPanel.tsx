
import React, { useState, useRef, useEffect } from 'react';
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { Play, Pause, Save, Upload, FileText, Book, Volume2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface EditorPanelProps {
  dyslexicMode: boolean;
}

const EditorPanel = ({ dyslexicMode }: EditorPanelProps) => {
  const [text, setText] = useState<string>("Enter your script here...");
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [currentWordIndex, setCurrentWordIndex] = useState<number>(-1);
  const [playbackRate, setPlaybackRate] = useState<number>(1);
  const [volume, setVolume] = useState<number>(1);
  const wordsRef = useRef<string[]>([]);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);
  const speechSynthRef = useRef<SpeechSynthesisUtterance | null>(null);
  const { toast } = useToast();

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
    // Check if browser supports speech synthesis
    if (!('speechSynthesis' in window)) {
      toast({
        title: "Speech synthesis not supported",
        description: "Your browser doesn't support text-to-speech functionality.",
        variant: "destructive"
      });
      return;
    }
    
    setIsPlaying(true);
    setCurrentWordIndex(0);
    
    // Cancel any previous speech
    window.speechSynthesis.cancel();
    
    // Create a new utterance for the current text
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = playbackRate;
    utterance.volume = volume;
    
    // Store the utterance reference
    speechSynthRef.current = utterance;
    
    // Set up event handlers
    utterance.onstart = () => {
      setIsPlaying(true);
    };
    
    utterance.onend = () => {
      setIsPlaying(false);
      setCurrentWordIndex(-1);
    };
    
    utterance.onpause = () => {
      setIsPlaying(false);
    };
    
    utterance.onresume = () => {
      setIsPlaying(true);
    };
    
    utterance.onboundary = (event) => {
      // This event fires whenever a word or sentence boundary is reached
      if (event.name === 'word') {
        // Calculate which word we're on based on the character index
        const textUpToChar = text.substring(0, event.charIndex);
        const wordCount = textUpToChar.split(/\s+/).length - 1;
        setCurrentWordIndex(wordCount);
      }
    };
    
    // Start speaking
    window.speechSynthesis.speak(utterance);
  };

  const stopPlayback = () => {
    setIsPlaying(false);
    setCurrentWordIndex(-1);
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    
    // Stop any active speech
    if (speechSynthRef.current) {
      window.speechSynthesis.cancel();
    }
  };

  // Clean up on component unmount
  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
      window.speechSynthesis.cancel();
    };
  }, []);

  // Update speech parameters when they change
  useEffect(() => {
    if (speechSynthRef.current && isPlaying) {
      // We need to restart speech with new parameters
      const currentIndex = currentWordIndex;
      stopPlayback();
      
      // Small timeout to ensure previous speech is fully canceled
      setTimeout(() => {
        setCurrentWordIndex(currentIndex);
        startPlayback();
      }, 100);
    }
  }, [playbackRate, volume]);

  // Initialize words on component mount
  useEffect(() => {
    wordsRef.current = text.split(/\s+/);
  }, []);

  // Render text with highlighted current word
  const renderText = () => {
    if (currentWordIndex === -1) return text;
    
    const words = text.split(/\s+/);
    return words.map((word, index) => (
      <span 
        key={index} 
        className={index === currentWordIndex ? "text-scriptGold font-bold" : ""}
      >
        {word}{' '}
      </span>
    ));
  };

  // Function to export audio (this is just a placeholder since we can't actually
  // download audio directly from the Web Speech API)
  const handleExportAudio = () => {
    toast({
      title: "Export Feature",
      description: "This would export your script as audio. The Web Speech API doesn't support direct export, but this is where you'd integrate a recording solution.",
    });
  };

  return (
    <div className="flex flex-col h-full w-full">
      <div className="flex-1 relative">
        {isPlaying ? (
          <div 
            className={`editor-container h-full w-full p-4 overflow-y-auto text-white ${dyslexicMode ? 'font-dyslexic' : 'font-inter'}`}
          >
            {renderText()}
          </div>
        ) : (
          <textarea
            className={`editor-container h-full w-full p-4 bg-black text-white resize-none outline-none border-none ${dyslexicMode ? 'font-dyslexic' : 'font-inter'}`}
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
              onClick={handleExportAudio}
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
        
        <div className="flex items-center space-x-4">
          <Volume2 className="h-4 w-4 text-scriptRed" />
          <span className="text-sm text-white">Volume:</span>
          <Slider
            value={[volume]}
            min={0}
            max={1}
            step={0.1}
            onValueChange={(values) => setVolume(values[0])}
            className="w-32"
          />
          <span className="text-sm text-white">{Math.round(volume * 100)}%</span>
        </div>
      </div>
    </div>
  );
};

export default EditorPanel;
