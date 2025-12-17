import React, {useState} from 'react';
import Chatbot from '@site/src/components/Chatbot';
import type {ReactNode} from 'react';

// Wrapper component to add chatbot to all pages
export default function Root({children}: {children: ReactNode}): ReactNode {
  const [isChatbotOpen, setIsChatbotOpen] = useState(false);

  return (
    <>
      {children}
      {/* Floating chatbot button and container - appears on all pages */}
      <div
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          zIndex: 1000,
        }}
      >
        {isChatbotOpen ? (
          <div
            style={{
              width: '400px',
              maxHeight: '600px',
              boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
              borderRadius: '8px',
              overflow: 'hidden',
            }}
          >
            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                padding: '8px 12px',
                backgroundColor: '#4f6fef',
                color: 'white',
                cursor: 'pointer',
              }}
              onClick={() => setIsChatbotOpen(false)}
            >
              <span style={{fontWeight: 'bold'}}>AI Assistant</span>
              <button
                style={{
                  background: 'none',
                  border: 'none',
                  color: 'white',
                  fontSize: '20px',
                  cursor: 'pointer',
                  padding: '0 8px',
                }}
                onClick={(e) => {
                  e.stopPropagation();
                  setIsChatbotOpen(false);
                }}
              >
                ×
              </button>
            </div>
            <Chatbot />
          </div>
        ) : (
          <button
            onClick={() => setIsChatbotOpen(true)}
            style={{
              width: '60px',
              height: '60px',
              borderRadius: '50%',
              backgroundColor: '#4f6fef',
              color: 'white',
              border: 'none',
              cursor: 'pointer',
              boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
              fontSize: '24px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'transform 0.2s',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'scale(1.1)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'scale(1)';
            }}
            title="Open AI Assistant"
          >
            💬
          </button>
        )}
      </div>
    </>
  );
}

