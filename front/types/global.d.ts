declare global {
    interface SpeechRecognitionResultList {
      readonly length: number;
      item(index: number): SpeechRecognitionResult;
      [index: number]: SpeechRecognitionResult;
    }
  
    interface SpeechRecognitionResult {
      readonly length: number;
      item(index: number): SpeechRecognitionAlternative;
      [index: number]: SpeechRecognitionAlternative;
      isFinal: boolean;
    }
  
    interface SpeechRecognitionAlternative {
      transcript: string;
      confidence: number;
    }
  
    interface SpeechRecognitionEvent extends Event {
      readonly results: SpeechRecognitionResultList;
      readonly resultIndex: number;
      readonly emma: Document | null;
      readonly interpretation: any;
    }
  
    interface SpeechRecognition extends EventTarget {
      continuous: boolean;
      interimResults: boolean;
      lang: string;
      start(): void;
      stop(): void;
      abort(): void;
      onresult: (event: SpeechRecognitionEvent) => void;
      onerror: (event: SpeechRecognitionErrorEvent) => void;
      onend: () => void;
    }
  
    interface SpeechRecognitionErrorEvent extends Event {
      error: string;
    }
  
    interface Window {
      SpeechRecognition: new () => SpeechRecognition;
      webkitSpeechRecognition: new () => SpeechRecognition;
    }
  }
  
export {}